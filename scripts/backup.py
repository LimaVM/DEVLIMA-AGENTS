#!/usr/bin/env python3
"""Root-only authenticated backup: PostgreSQL, app secrets and manager metadata, no guest disks."""

import argparse
import json
import os
import sqlite3
import subprocess
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from backup_crypto import encrypt, sha256

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path("/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2")
TEMPLATE_SHA256 = "6a81c37564db9b1ee84e141922625e1d7c5b389b99bb3c572e0243607d5bb4d2"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", default="/etc/devlima-backup.key")
    parser.add_argument(
        "--include-template",
        action="store_true",
        help="Include the immutable base image for host recovery",
    )
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit("Run as root; backup never prints credentials.")
    if args.include_template and sha256(TEMPLATE) != TEMPLATE_SHA256:
        raise ValueError("Template differs from the inspected base image")
    os.umask(0o077)
    values = dict(
        line.split("=", 1)
        for line in (ROOT / ".env").read_text().splitlines()
        if line and not line.startswith("#") and "=" in line
    )
    compose = [
        "docker",
        "compose",
        "--env-file",
        str(ROOT / ".env"),
        "-f",
        str(ROOT / "infra/docker-compose.yml"),
    ]
    destination = ROOT / "backups"
    destination.mkdir(mode=0o700, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    archive = destination / f"devlima-{stamp}.dlag"
    with tempfile.TemporaryDirectory(prefix="devlima-backup-") as temporary:
        folder = Path(temporary)
        dump = folder / "postgres.dump"
        with dump.open("wb") as output:
            subprocess.run(
                [
                    *compose,
                    "exec",
                    "--interactive=false",
                    "postgres",
                    "pg_dump",
                    "-U",
                    values["POSTGRES_USER"],
                    "-d",
                    values["POSTGRES_DB"],
                    "-Fc",
                ],
                stdout=output,
                check=True,
            )
        registry = Path("/var/lib/devlima-vm-manager/registry.sqlite3")
        if registry.exists():
            with (
                sqlite3.connect(registry) as source,
                sqlite3.connect(folder / "manager.sqlite3") as target,
            ):
                source.backup(target)
        manifest = {
            "created_at": datetime.now(UTC).isoformat(),
            "git_commit": subprocess.check_output(
                ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
            ).strip(),
            "postgres_dump_sha256": sha256(dump),
            "format": 1,
            "guest_images_included": False,
            "template_included": args.include_template,
            "template_sha256": TEMPLATE_SHA256,
        }
        (folder / "manifest.json").write_text(json.dumps(manifest, indent=2))
        plain = folder / "backup.tar"
        with tarfile.open(plain, "w", dereference=True) as tar:
            tar.add(dump, arcname="postgres.dump")
            tar.add(folder / "manifest.json", arcname="manifest.json")
            for source, name in [
                (ROOT / ".env", "config/core.env"),
                (ROOT / "backups/operator-credentials.json", "config/operator-credentials.json"),
                (Path("/etc/devlima-vm-manager.env"), "config/manager.env"),
                (Path("/root/.ssh/agent_worker"), "config/agent_worker"),
                (Path("/root/.ssh/agent_worker.pub"), "config/agent_worker.pub"),
                (folder / "manager.sqlite3", "manager.sqlite3"),
                (Path("/srv/devlima-build-tools/signing.properties"), "config/signing.properties"),
                (Path("/srv/devlima-build-tools/agent-release.jks"), "config/agent-release.jks"),
            ]:
                if source.is_file():
                    tar.add(source, arcname=name, recursive=False)
            if args.include_template:
                tar.add(TEMPLATE, arcname="templates/ubuntu-24.04-base.qcow2", recursive=False)
        if args.include_template and sha256(TEMPLATE) != TEMPLATE_SHA256:
            raise ValueError("Template changed while creating the backup")
        encrypt(plain, archive, args.key)
    checksum = archive.with_suffix(".sha256")
    digest = sha256(archive)
    checksum.write_text(digest + "  " + archive.name + "\n")
    for path in (archive, checksum):
        os.chown(path, ROOT.stat().st_uid, ROOT.stat().st_gid)
        os.chmod(path, 0o600)
    # Retention affects only automatically named encrypted archives and their checksums.
    for old in sorted(destination.glob("devlima-????????T??????Z.dlag"))[:-14]:
        old.unlink()
        old.with_suffix(".sha256").unlink(missing_ok=True)
    print(json.dumps({"backup": str(archive), "encrypted": True, "sha256": digest}))


if __name__ == "__main__":
    main()
