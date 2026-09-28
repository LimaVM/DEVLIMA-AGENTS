"""Install private VM Manager as root on the already inspected Ubuntu host."""

import argparse
import grp
import os
import secrets
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path


def run(args):
    subprocess.run(args, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path("/srv/devlima-agent"))
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit("Run as root on the VM host")
    try:
        grp.getgrgid(10001)
    except KeyError:
        run(["groupadd", "--system", "--gid", "10001", "devlima-core"])
    project = args.project.resolve(strict=True)
    source = project / "vm-manager"
    destination = Path("/opt/devlima-vm-manager")
    destination.mkdir(mode=0o755, exist_ok=True)
    shutil.copytree(source / "vm_manager", destination / "vm_manager", dirs_exist_ok=True)
    shutil.copyfile(source / "requirements.txt", destination / "requirements.txt")
    for directory in (Path("/var/lib/libvirt/images/devlima-workers"),):
        directory.mkdir(parents=True, exist_ok=True, mode=0o755)
        directory.chmod(0o755)
    state = Path("/var/lib/devlima-vm-manager")
    state.mkdir(mode=0o700, exist_ok=True)
    state.chmod(0o700)
    config = Path("/etc/devlima-vm-manager.env")
    token = None
    if config.exists():
        for line in config.read_text().splitlines():
            if line.startswith("VM_MANAGER_TOKEN="):
                token = line.split("=", 1)[1]
    if token is None:
        token = secrets.token_urlsafe(48)
        descriptor = os.open(config, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w") as output:
            output.write("VM_MANAGER_TOKEN=" + token + "\n")
    if len(token) < 32 or any(
        char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        for char in token
    ):
        raise SystemExit("Invalid existing manager token")
    config.chmod(0o600)
    env = project / ".env"
    content = [
        line for line in env.read_text().splitlines() if not line.startswith("VM_MANAGER_TOKEN=")
    ]
    env.chmod(0o600)
    env.write_text("\n".join(content) + "\nVM_MANAGER_TOKEN=" + token + "\n")
    venv = destination / "venv"
    if not (venv / "bin/python").exists():
        run(["/usr/bin/python3", "-m", "venv", "--system-site-packages", str(venv)])
    run(
        [
            str(venv / "bin/pip"),
            "install",
            "--disable-pip-version-check",
            "-r",
            str(destination / "requirements.txt"),
        ]
    )
    shutil.copyfile(
        source / "systemd/devlima-vm-manager.service",
        "/etc/systemd/system/devlima-vm-manager.service",
    )
    filter_xml = ET.parse(source / "systemd/devlima-worker-egress.xml").getroot()
    existing_filter = subprocess.run(
        ["virsh", "nwfilter-dumpxml", "devlima-worker-egress"], capture_output=True, check=False
    )
    if existing_filter.returncode == 0:
        ET.SubElement(filter_xml, "uuid").text = ET.fromstring(existing_filter.stdout).findtext(
            "uuid"
        )
    filter_file = state / "worker-filter.xml"
    filter_file.write_text(ET.tostring(filter_xml, encoding="unicode"))
    run(["virsh", "nwfilter-define", str(filter_file)])
    run(["systemctl", "daemon-reload"])
    run(["systemctl", "enable", "devlima-vm-manager.service"])
    run(["systemctl", "restart", "devlima-vm-manager.service"])
    for _ in range(30):
        if Path("/run/devlima-vm-manager/api.sock").exists():
            break
        time.sleep(1)
    else:
        raise SystemExit("Manager socket did not appear; inspect systemd diagnostics")
    Path("/run/devlima-vm-manager/api.sock").chmod(0o660)
    print("Private VM Manager installed; token retained in protected env files only.")


if __name__ == "__main__":
    main()
