#!/usr/bin/env python3
"""Authenticate/decrypt backup and restore ONLY into a unique temporary validation database."""

import argparse
import json
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path
from uuid import uuid4

from backup_crypto import decrypt, sha256

ROOT = Path(__file__).resolve().parents[1]


# Documentação: Coordena a entrada de linha de comando deste arquivo: Decifra backup e valida
# restore em banco temporário exclusivo; verifica pacote/template e remove o banco de validação ao
# terminar.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--key", default="/etc/devlima-backup.key")
    parser.add_argument(
        "--extract-to",
        type=Path,
        help="Extract verified files into a NEW private directory; preserve production",
    )
    args = parser.parse_args()
    os.umask(0o077)
    with tempfile.TemporaryDirectory(prefix="devlima-restore-") as temporary:
        folder = Path(temporary)
        plain = folder / "backup.tar"
        decrypt(args.archive, plain, args.key)
        target = args.extract_to or folder / "extracted"
        target.mkdir(mode=0o700, parents=False, exist_ok=False)
        with tarfile.open(plain) as tar:
            for member in tar:
                if (
                    not member.isfile()
                    or Path(member.name).is_absolute()
                    or ".." in Path(member.name).parts
                ):
                    raise ValueError("Unsafe backup member")
                path = target / member.name
                path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                source = tar.extractfile(member)
                with path.open("xb") as output:
                    while block := source.read(1024 * 1024):
                        output.write(block)
                path.chmod(0o600)
        manifest = json.loads((target / "manifest.json").read_text())
        if sha256(target / "postgres.dump") != manifest["postgres_dump_sha256"]:
            raise ValueError("PostgreSQL dump checksum mismatch")
        if manifest.get("template_included") and (
            sha256(target / "templates/ubuntu-24.04-base.qcow2") != manifest["template_sha256"]
        ):
            raise ValueError("Template checksum mismatch")
        if args.extract_to:
            print("Backup authenticated and extracted privately; production files preserved.")
            return
        values = dict(
            line.split("=", 1)
            for line in (ROOT / ".env").read_text().splitlines()
            if line and not line.startswith("#") and "=" in line
        )
        database = "restore_validation_" + uuid4().hex
        assert database != values["POSTGRES_DB"] and database.startswith("restore_validation_")
        compose = [
            "sudo",
            "docker",
            "compose",
            "--env-file",
            str(ROOT / ".env"),
            "-f",
            str(ROOT / "infra/docker-compose.yml"),
            "exec",
            "-T",
            "postgres",
        ]
        user = values["POSTGRES_USER"]
        created = False
        try:
            subprocess.run([*compose, "createdb", "-U", user, database], check=True)
            created = True
            with (target / "postgres.dump").open("rb") as input_file:
                subprocess.run(
                    [
                        *compose,
                        "pg_restore",
                        "--exit-on-error",
                        "--no-owner",
                        "--no-acl",
                        "-U",
                        user,
                        "-d",
                        database,
                    ],
                    stdin=input_file,
                    check=True,
                )
            query = "SELECT version_num FROM alembic_version; SELECT 'users',count(*) FROM users; SELECT 'messages',count(*) FROM messages; SELECT 'schedules',count(*) FROM schedules; SELECT 'call_sessions',count(*) FROM call_sessions;"  # noqa: E501
            output = subprocess.check_output(
                [*compose, "psql", "-U", user, "-d", database, "-At", "-c", query], text=True
            )
            assert "0007_calls" in output
            print("Authenticated restore passed in isolated database:\n" + output.strip())
        finally:
            if created:
                subprocess.run([*compose, "dropdb", "-U", user, database], check=True)


if __name__ == "__main__":
    main()
