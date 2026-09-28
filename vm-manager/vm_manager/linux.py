import hashlib
import ipaddress
import json
import os
import pwd
import selectors
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import UUID

from vm_manager.config import VMError

METADATA_NS = "urn:devlima:worker:1"


def command(arguments, timeout=90, input=None):
    try:
        result = subprocess.run(
            arguments, input=input, capture_output=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        raise VMError("host_operation_timeout", 504) from None
    if result.returncode:
        raise VMError("host_operation_failed", 503)
    return result.stdout


class LinuxWorkerProvider:
    def __init__(self, settings):
        import libvirt

        self.libvirt = libvirt
        self.settings = settings
        self.root = settings.worker_root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.template = settings.template.resolve(strict=True)
        if self.template.is_relative_to(self.root):
            raise VMError("unsafe_template_path", 503)
        if self.hash_file(self.template) != settings.template_sha256:
            raise VMError("template_checksum_mismatch", 503)
        self.template_stat = (self.template.stat().st_size, self.template.stat().st_mtime_ns)
        self.conn = libvirt.open("qemu:///system")
        self.qemu = pwd.getpwnam("libvirt-qemu")
        self.conn.nwfilterLookupByName("devlima-worker-egress")

    def close(self):
        self.conn.close()

    def hash_file(self, path):
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def directory(self, identifier):
        identifier = str(UUID(str(identifier)))
        raw = self.root / identifier
        if raw.is_symlink() or not raw.resolve().is_relative_to(self.root):
            raise VMError("unsafe_worker_path", 422)
        return raw

    def path(self, identifier, name):
        base = self.directory(identifier)
        target = base / name
        if target.is_symlink() or not target.resolve().is_relative_to(base.resolve()):
            raise VMError("unsafe_worker_path", 422)
        return target

    def own_file(self, path):
        os.chown(path, self.qemu.pw_uid, self.qemu.pw_gid)
        path.chmod(0o660)

    def domain(self, row, missing=False):
        try:
            domain = self.conn.lookupByUUIDString(row["id"])
        except self.libvirt.libvirtError as error:
            if missing and error.get_error_code() == self.libvirt.VIR_ERR_NO_DOMAIN:
                return None
            raise VMError("domain_not_found", 404) from None
        root = ET.fromstring(domain.XMLDesc(0))
        metadata = root.find(f"metadata/{{{METADATA_NS}}}worker")
        if (
            metadata is None
            or metadata.attrib.get("id") != row["id"]
            or metadata.attrib.get("owner") != row["owner"]
        ):
            raise VMError("foreign_domain_protected", 403)
        disk = root.find("devices/disk[@device='disk']/source")
        if (
            disk is None
            or Path(disk.attrib.get("file", "")).resolve()
            != self.path(row["id"], "disk.qcow2").resolve()
        ):
            raise VMError("foreign_storage_protected", 403)
        return domain

    def check_resources(self, rows, desired):
        active = [row for row in rows if row["status"] != "DESTROYED"]
        config = self.settings
        if (
            len(active) >= config.max_workers
            or sum(row["vcpu"] for row in active) + desired["vcpu"] > config.max_total_vcpu
            or sum(row["ram_mb"] for row in active) + desired["ram_mb"] > config.max_total_ram_mb
        ):
            raise VMError("worker_quota_exceeded", 429)
        memory = dict(line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines())
        available = int(memory["MemAvailable"].split()[0]) // 1024
        if available - desired["ram_mb"] < config.host_ram_reserve_mb:
            raise VMError("host_memory_reserve", 429)
        existing_vcpu = sum(
            domain.info()[3]
            for domain in self.conn.listAllDomains(self.libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
        )
        if existing_vcpu + desired["vcpu"] > max(1, (os.cpu_count() or 1) - 1):
            raise VMError("host_cpu_reserve", 429)
        reserved = sum(row["disk_gb"] for row in active)
        if (
            shutil.disk_usage(self.root).free
            < (reserved + desired["disk_gb"] + config.disk_reserve_gb) * 1024**3
        ):
            raise VMError("host_disk_reserve", 429)

    def make_xml(self, row, disk, seed):
        domain = ET.Element("domain", type="kvm")
        ET.SubElement(domain, "name").text = f"devlima-{UUID(row['id']).hex}"
        ET.SubElement(domain, "uuid").text = row["id"]
        ET.SubElement(domain, "memory", unit="MiB").text = str(row["ram_mb"])
        ET.SubElement(domain, "vcpu").text = str(row["vcpu"])
        os_node = ET.SubElement(domain, "os")
        ET.SubElement(os_node, "type", arch="x86_64", machine="q35").text = "hvm"
        ET.SubElement(os_node, "boot", dev="hd")
        features = ET.SubElement(domain, "features")
        ET.SubElement(features, "acpi")
        ET.SubElement(features, "apic")
        ET.SubElement(domain, "cpu", mode="host-passthrough")
        metadata = ET.SubElement(domain, "metadata")
        ET.SubElement(
            metadata,
            f"{{{METADATA_NS}}}worker",
            id=row["id"],
            owner=row["owner"],
            generation=row["generation"],
        )
        devices = ET.SubElement(domain, "devices")
        drive = ET.SubElement(devices, "disk", type="file", device="disk")
        ET.SubElement(drive, "driver", name="qemu", type="qcow2")
        ET.SubElement(drive, "source", file=str(disk))
        ET.SubElement(drive, "target", dev="vda", bus="virtio")
        cloud = ET.SubElement(devices, "disk", type="file", device="cdrom")
        ET.SubElement(cloud, "driver", name="qemu", type="raw")
        ET.SubElement(cloud, "source", file=str(seed))
        ET.SubElement(cloud, "target", dev="sda", bus="sata")
        ET.SubElement(cloud, "readonly")
        interface = ET.SubElement(devices, "interface", type="network")
        mac = "52:54:00:" + ":".join(f"{value:02x}" for value in UUID(row["id"]).bytes[-3:])
        ET.SubElement(interface, "mac", address=mac)
        ET.SubElement(interface, "source", network=self.settings.network)
        ET.SubElement(interface, "model", type="virtio")
        ET.SubElement(interface, "filterref", filter="devlima-worker-egress")
        channel = ET.SubElement(devices, "channel", type="unix")
        ET.SubElement(channel, "target", type="virtio", name="org.qemu.guest_agent.0")
        ET.SubElement(devices, "console", type="pty")
        ET.SubElement(devices, "memballoon", model="virtio")
        return ET.tostring(domain, encoding="unicode")

    def create(self, row):
        if (self.template.stat().st_size, self.template.stat().st_mtime_ns) != self.template_stat:
            raise VMError("template_changed", 503)
        directory = self.directory(row["id"])
        directory.mkdir(mode=0o755, exist_ok=True)
        directory.chmod(0o755)
        disk, seed = self.path(row["id"], "disk.qcow2"), self.path(row["id"], "seed.iso")
        if not disk.exists():
            command(
                [
                    "/usr/bin/qemu-img",
                    "create",
                    "-f",
                    "qcow2",
                    "-F",
                    "qcow2",
                    "-b",
                    str(self.template),
                    str(disk),
                    f"{row['disk_gb']}G",
                ]
            )
            self.own_file(disk)
        public_key = self.settings.ssh_public_key.read_text().strip()
        if not public_key.startswith(("ssh-ed25519 ", "ssh-rsa ")):
            raise VMError("invalid_worker_public_key", 503)
        config = {
            "hostname": f"worker-{UUID(row['id']).hex[:12]}",
            "manage_etc_hosts": True,
            "users": [
                {
                    "name": "agent",
                    "groups": ["sudo"],
                    "shell": "/bin/bash",
                    "lock_passwd": True,
                    "sudo": "ALL=(ALL) NOPASSWD:ALL",
                    "ssh_authorized_keys": [public_key],
                }
            ],
            "ssh_pwauth": False,
            "disable_root": True,
            "package_update": True,
            "packages": [
                "qemu-guest-agent",
                "openssh-server",
                "curl",
                "wget",
                "git",
                "python3",
                "python3-pip",
            ],
            "growpart": {"mode": "auto", "devices": ["/"], "ignore_growroot_disabled": False},
            "resize_rootfs": True,
            "runcmd": [["systemctl", "enable", "--now", "qemu-guest-agent"]],
        }
        user_data, meta_data = self.path(row["id"], "user-data"), self.path(row["id"], "meta-data")
        user_data.write_text("#cloud-config\n" + json.dumps(config))
        meta_data.write_text(
            json.dumps({"instance-id": row["generation"], "local-hostname": config["hostname"]})
        )
        command(["/usr/bin/cloud-localds", str(seed), str(user_data), str(meta_data)])
        self.own_file(seed)
        domain = self.domain(row, missing=True)
        if domain is None:
            domain = self.conn.defineXML(self.make_xml(row, disk, seed))
        if not domain.isActive():
            domain.create()
        return {**row, "status": "BOOTING", "ip": None}

    def ip(self, domain):
        root = ET.fromstring(domain.XMLDesc(0))
        mac = root.find("devices/interface/mac").attrib["address"]
        for lease in self.conn.networkLookupByName(self.settings.network).DHCPLeases(mac, 0):
            try:
                address = ipaddress.ip_address(lease["ipaddr"])
                if (
                    address in ipaddress.ip_network("192.168.122.0/24")
                    and int(str(address).split(".")[-1]) > 1
                ):
                    return str(address)
            except (ValueError, KeyError):
                pass
        return None

    def ssh_args(self, row, remote_command):
        hosts = self.settings.state_root / f"known-{row['id']}"
        return [
            "/usr/bin/ssh",
            "-o",
            "BatchMode=yes",
            "-o",
            "LogLevel=ERROR",
            "-o",
            "StrictHostKeyChecking=accept-new",
            "-o",
            f"UserKnownHostsFile={hosts}",
            "-o",
            "ConnectTimeout=3",
            "-i",
            str(self.settings.ssh_private_key),
            f"agent@{row['ip']}",
            remote_command,
        ]

    def status(self, row):
        if row["status"] == "DESTROYED":
            return row
        domain = self.domain(row, missing=True)
        if domain is None:
            return {**row, "status": "ERROR", "ip": None, "error_code": "domain_missing"}
        if not domain.isActive():
            return {**row, "status": "STOPPED", "ip": None}
        address = self.ip(domain)
        state = {**row, "ip": address}
        if not address:
            return {**state, "status": "BOOTING"}
        try:
            command(
                self.ssh_args(
                    state,
                    "test -f /var/lib/cloud/instance/boot-finished && "
                    "systemctl is-active --quiet qemu-guest-agent",
                ),
                timeout=5,
            )
            domain.interfaceAddresses(self.libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
        except (VMError, self.libvirt.libvirtError):
            return {**state, "status": "BOOTING"}
        return {**state, "status": "READY", "error_code": None}

    def stop(self, row):
        domain = self.domain(row, missing=True)
        running = bool(domain and domain.isActive())
        if running:
            try:
                domain.shutdown()
            except self.libvirt.libvirtError:
                pass
            deadline = time.monotonic() + 45
            while domain.isActive() and time.monotonic() < deadline:
                time.sleep(1)
            if domain.isActive():
                domain.destroy()
        return running

    def start(self, row):
        domain = self.domain(row)
        if not domain.isActive():
            domain.create()
        return {**row, "status": "BOOTING", "ip": None}

    def destroy(self, row):
        self.stop(row)
        domain = self.domain(row, missing=True)
        if domain:
            domain.undefine()
        directory = self.directory(row["id"])
        if directory.exists():
            shutil.rmtree(directory)
        (self.settings.state_root / f"known-{row['id']}").unlink(missing_ok=True)
        return {**row, "status": "DESTROYED", "ip": None}

    def reset(self, row, generation):
        self.stop(row)
        domain = self.domain(row, missing=True)
        if domain:
            domain.undefine()
        for name in ("disk.qcow2", "seed.iso", "user-data", "meta-data"):
            self.path(row["id"], name).unlink(missing_ok=True)
        (self.settings.state_root / f"known-{row['id']}").unlink(missing_ok=True)
        return self.create({**row, "generation": generation})

    def snapshot(self, row, identifier):
        destination = self.path(row["id"], f"snapshots/{UUID(str(identifier))}.qcow2")
        destination.parent.mkdir(mode=0o755, exist_ok=True)
        destination.parent.chmod(0o755)
        if destination.exists():
            raise VMError("snapshot_already_exists")
        if (
            shutil.disk_usage(self.root).free
            < (row["disk_gb"] + self.settings.disk_reserve_gb) * 1024**3
        ):
            raise VMError("host_disk_reserve", 429)
        running = self.stop(row)
        command(
            [
                "/usr/bin/qemu-img",
                "convert",
                "-m",
                "1",
                "-t",
                "none",
                "-T",
                "none",
                "-f",
                "qcow2",
                "-O",
                "qcow2",
                str(self.path(row["id"], "disk.qcow2")),
                str(destination),
            ],
            timeout=120,
        )
        self.own_file(destination)
        data = {
            "id": str(identifier),
            "worker_id": row["id"],
            "sha256": self.hash_file(destination),
        }
        return data, self.start(row) if running else {**row, "status": "STOPPED", "ip": None}

    def restore(self, row, snapshot):
        source = self.path(row["id"], f"snapshots/{UUID(snapshot['id'])}.qcow2")
        if not source.is_file() or self.hash_file(source) != snapshot["sha256"]:
            raise VMError("snapshot_checksum_mismatch")
        running = self.stop(row)
        temporary = self.path(row["id"], "restore.tmp")
        command(
            [
                "/usr/bin/qemu-img",
                "convert",
                "-m",
                "1",
                "-t",
                "none",
                "-T",
                "none",
                "-f",
                "qcow2",
                "-O",
                "qcow2",
                str(source),
                str(temporary),
            ],
            timeout=120,
        )
        self.own_file(temporary)
        temporary.replace(self.path(row["id"], "disk.qcow2"))
        (self.settings.state_root / f"known-{row['id']}").unlink(missing_ok=True)
        return self.start(row) if running else {**row, "status": "STOPPED", "ip": None}

    def execute(self, row, identifier, script, timeout):
        state = self.status(row)
        if state["status"] != "READY":
            raise VMError("worker_not_ready")
        remote = (
            "sudo systemd-run --quiet --wait --pipe --collect "
            f"--unit=devlima-job-{UUID(str(identifier)).hex} "
            f"--property=RuntimeMaxSec={timeout} "
            "--property=MemoryMax=512M --property=TasksMax=256 /bin/bash -s"
        )
        process = subprocess.Popen(
            self.ssh_args(state, remote),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        process.stdin.write(script.encode())
        process.stdin.close()
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        output, truncated = bytearray(), False
        deadline = time.monotonic() + timeout + 15
        try:
            while selector.get_map():
                if time.monotonic() > deadline:
                    process.kill()
                    raise VMError("worker_job_timeout", 504)
                for key, _ in selector.select(1):
                    chunk = os.read(key.fileobj.fileno(), 4096)
                    if not chunk:
                        selector.unregister(key.fileobj)
                    else:
                        space = 16000 - len(output)
                        output.extend(chunk[: max(0, space)])
                        truncated |= len(chunk) > space
            code = process.wait(timeout=5)
        finally:
            selector.close()
            if process.poll() is None:
                process.kill()
            process.wait(timeout=5)
            process.stdout.close()
        return {
            "exit_code": code,
            "output": output.decode(errors="replace"),
            "truncated": truncated,
        }


class WindowsWorkerProvider:
    def create(self, *_):
        raise VMError("windows_not_available", 501)

    check_resources = create
    status = create
    start = create
    stop = create
    destroy = create
    reset = create
    snapshot = create
    restore = create
    execute = create

    def close(self):
        pass
