#!/usr/bin/env python3
"""Pull authenticated, encrypted backups over existing SSH; suitable for macOS launchd."""

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
from pathlib import Path

REMOTE_PROGRAM = (
    "import json;from pathlib import Path;root=Path('/srv/devlima-agent/backups');"
    "print(json.dumps([{'name':p.name,'checksum':p.with_suffix('.sha256').read_text().split()[0]} "
    "for p in sorted(root.glob('devlima-*.dlag')) if p.with_suffix('.sha256').exists()]))"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="ubuntu@147.15.33.140")
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z_][a-z0-9_-]*@[a-zA-Z0-9.-]+", args.host):
        parser.error("Use user@hostname without SSH options")
    os.umask(0o077)
    args.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    args.directory.chmod(0o700)
    options = [
        "-i",
        str(args.key),
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=yes",
        "-o",
        "ConnectTimeout=10",
    ]
    result = subprocess.check_output(
        ["ssh", *options, args.host, "python3 -c " + shlex.quote(REMOTE_PROGRAM)], text=True
    )
    entries = json.loads(result)
    downloaded = 0
    for entry in entries:
        name, expected = entry["name"], entry["checksum"]
        if not re.fullmatch(r"devlima-\d{8}T\d{6}Z\.dlag", name) or not re.fullmatch(
            r"[a-f0-9]{64}", expected
        ):
            raise ValueError("Unexpected remote backup metadata")
        target = args.directory / name
        if target.exists():
            continue
        temporary = target.with_suffix(".partial")
        subprocess.run(
            ["scp", *options, args.host + ":/srv/devlima-agent/backups/" + name, str(temporary)],
            check=True,
        )
        temporary.chmod(0o600)
        digest = hashlib.sha256()
        with temporary.open("rb") as source:
            while block := source.read(1024 * 1024):
                digest.update(block)
        if digest.hexdigest() != expected:
            temporary.unlink()
            raise ValueError("Backup checksum mismatch")
        temporary.replace(target)
        target.with_suffix(".sha256").write_text(expected + "  " + name + "\n")
        downloaded += 1
    print(
        json.dumps(
            {
                "copied": downloaded,
                "remote_archives": len(entries),
                "directory": str(args.directory),
            }
        )
    )


if __name__ == "__main__":
    main()
