"""Exercise only a newly created managed worker, via the private API. Run on VPS as root."""

import hashlib
import http.client
import json
import socket
import time
from pathlib import Path
from uuid import uuid4


class UnixConnection(http.client.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(350)
        self.sock.connect("/run/devlima-vm-manager/api.sock")


def main():
    token = next(
        line.split("=", 1)[1]
        for line in Path("/etc/devlima-vm-manager.env").read_text().splitlines()
        if line.startswith("VM_MANAGER_TOKEN=")
    )
    owner, worker = str(uuid4()), str(uuid4())
    template = Path("/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2")
    digest = hashlib.sha256(template.read_bytes()).hexdigest()
    calls = []

    def request(method, path, data=None, authenticate=True):
        connection = UnixConnection("vm-manager")
        headers = {"Content-Type": "application/json"}
        if authenticate:
            headers["Authorization"] = "Bearer " + token
        try:
            connection.request(method, path, json.dumps(data) if data else None, headers)
            response = connection.getresponse()
            payload = json.loads(response.read())
            return response.status, payload
        finally:
            connection.close()

    def operation(kind, **args):
        data = {
            "request_id": str(uuid4()),
            "worker_id": worker,
            "owner": owner,
            "kind": kind,
            **args,
        }
        status, result = request("POST", "/v1/operations", data)
        if status != 200:
            raise RuntimeError(f"{kind} failed: {status} {result}")
        calls.append(kind)
        print(
            json.dumps({"operation": kind, "status": result.get("worker", {}).get("status")}),
            flush=True,
        )
        return result, data

    def ready():
        deadline = time.monotonic() + 900
        last, heartbeat = None, 0
        while time.monotonic() < deadline:
            status, row = request("GET", f"/v1/workers/{worker}?owner={owner}")
            if status != 200:
                raise RuntimeError("Worker status unavailable")
            if row["status"] != last or time.monotonic() > heartbeat:
                print(json.dumps({"status": row["status"], "ip": row.get("ip")}), flush=True)
                heartbeat, last = time.monotonic() + 60, row["status"]
            if row["status"] == "READY":
                return
            if row["status"] in {"ERROR", "DESTROYED"}:
                raise RuntimeError("Worker entered failure state")
            time.sleep(5)
        raise RuntimeError("Cloud-init/guest-agent did not become ready within 15 minutes")

    assert request("GET", "/health", authenticate=False)[0] == 401
    created = False
    try:
        _, create = operation("CREATE", name="phase5-smoke", vcpu=2, ram_mb=2048, disk_gb=20)
        created = True
        repeat, _ = request("POST", "/v1/operations", create)
        assert repeat == 200
        assert request("GET", f"/v1/workers/{worker}?owner={uuid4()}")[0] == 404
        ready()
        result, execution = operation(
            "EXECUTE",
            script="printf original > /home/agent/phase5-marker\ncat /home/agent/phase5-marker\n",
            timeout=30,
        )
        assert result["job"]["exit_code"] == 0 and result["job"]["output"].strip() == "original"
        assert request("POST", "/v1/operations", execution)[1] == result
        # Managed network filter denies metadata and host/private-network initiation.
        result, _ = operation(
            "EXECUTE",
            script=(
                "metadata=$(curl --noproxy '*' --max-time 3 -s "
                "-o /dev/null -w '%{http_code}' "
                "-H 'Authorization: Bearer Oracle' "
                "http://169.254.169.254/opc/v2/instance/ 2>/dev/null || true)\n"
                'test "$metadata" = 000 || exit 90\n'
                "core=$(curl --noproxy '*' --max-time 3 -s -o /dev/null -w '%{http_code}' "
                "http://147.15.33.140/ 2>/dev/null || true)\n"
                'test "$core" = 000 || exit 91\n'
                "private=$(curl --noproxy '*' --max-time 3 -s -o /dev/null -w '%{http_code}' "
                "http://100.108.84.64/ 2>/dev/null || true)\n"
                'test "$private" = 000 || exit 92\n'
                "printf isolation-ok\n"
            ),
            timeout=15,
        )
        assert result["job"]["exit_code"] == 0 and "isolation-ok" in result["job"]["output"]
        snapshot = str(uuid4())
        operation("SNAPSHOT", snapshot_id=snapshot)
        ready()
        result, _ = operation(
            "EXECUTE", script="printf changed > /home/agent/phase5-marker", timeout=30
        )
        assert result["job"]["exit_code"] == 0
        operation("RESTORE", snapshot_id=snapshot)
        ready()
        result, _ = operation("EXECUTE", script="cat /home/agent/phase5-marker", timeout=30)
        assert result["job"]["exit_code"] == 0 and result["job"]["output"].strip() == "original"
        operation("STOP")
        operation("START")
        ready()
        operation("RESET")
        ready()
        result, _ = operation(
            "EXECUTE",
            script="test ! -e /home/agent/phase5-marker && printf reset-clean",
            timeout=30,
        )
        assert result["job"]["exit_code"] == 0 and "reset-clean" in result["job"]["output"]
    finally:
        if created:
            operation("DESTROY")
            assert not (Path("/var/lib/libvirt/images/devlima-workers") / worker).exists()
        assert hashlib.sha256(template.read_bytes()).hexdigest() == digest
    print(
        json.dumps(
            {
                "result": "passed",
                "worker_id": worker,
                "operations": calls,
                "template_sha256": digest,
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
