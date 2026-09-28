#!/usr/bin/env python3
"""Provision least-privilege roles through private Docker stdin; never print secrets."""

import json
import os
import secrets
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = [
    "sudo",
    "docker",
    "compose",
    "--env-file",
    str(ROOT / ".env"),
    "-f",
    str(ROOT / "infra/docker-compose.yml"),
]


# Documentação: Coordena a entrada de linha de comando deste arquivo: Cria/atualiza credenciais
# externas de papéis PostgreSQL e aplica separação de permissões; preserva .env anterior em caso
# de falha.
def main():
    env = ROOT / ".env"
    assert env.exists() and env.stat().st_mode & 0o077 == 0, ".env must be private"
    original = env.read_text()
    values = dict(
        line.split("=", 1)
        for line in original.splitlines()
        if line and not line.startswith("#") and "=" in line
    )
    additions = {
        "RUNTIME_POSTGRES_USER": "agent_runtime",
        "MIGRATION_POSTGRES_USER": "agent_migrate",
        "RUNTIME_POSTGRES_PASSWORD": secrets.token_hex(32),
        "MIGRATION_POSTGRES_PASSWORD": secrets.token_hex(32),
    }
    missing = {key: value for key, value in additions.items() if not values.get(key)}
    values.update(missing)
    if missing:
        temporary = env.with_suffix(".private-new")
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w") as output:
            output.write(
                original.rstrip()
                + "\n"
                + "\n".join(f"{key}={value}" for key, value in missing.items())
                + "\n"
            )
        temporary.replace(env)
    result = subprocess.run(
        [
            *COMPOSE,
            "--profile",
            "ops",
            "run",
            "--rm",
            "--no-deps",
            "-T",
            "db-admin",
            "python",
            "-m",
            "app.db.provision",
        ],
        input=json.dumps(
            {
                key: values[key]
                for key in (
                    "POSTGRES_DB",
                    "POSTGRES_USER",
                    "POSTGRES_PASSWORD",
                    "RUNTIME_POSTGRES_USER",
                    "RUNTIME_POSTGRES_PASSWORD",
                    "MIGRATION_POSTGRES_USER",
                    "MIGRATION_POSTGRES_PASSWORD",
                )
            }
        ),
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise SystemExit(
            "Role provisioning failed; no credentials displayed. Preserve .env and previous backup."
        )
    print(result.stdout.strip())


if __name__ == "__main__":
    main()
