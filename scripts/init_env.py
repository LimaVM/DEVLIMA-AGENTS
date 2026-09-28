#!/usr/bin/env python3
"""Generate secrets without stdout disclosure or overwriting an existing .env."""
import argparse
import os
import re
import secrets
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Public hostname already pointing to this host")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    values = (root / ".env.example").read_text()
    values = values.replace("POSTGRES_PASSWORD=\n", f"POSTGRES_PASSWORD={secrets.token_hex(32)}\n")
    values = values.replace("JWT_SECRET=\n", f"JWT_SECRET={secrets.token_hex(48)}\n")
    values = values.replace("VM_MANAGER_TOKEN=\n", f"VM_MANAGER_TOKEN={secrets.token_hex(32)}\n")
    if args.domain:
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?", args.domain):
            parser.error("Domínio inválido")
        for previous, updated in {
            "AGENT_DOMAIN=localhost": f"AGENT_DOMAIN={args.domain}",
            "CADDY_CONFIG=Caddyfile.private": "CADDY_CONFIG=Caddyfile",
            "CADDY_BIND=127.0.0.1": "CADDY_BIND=0.0.0.0",
            "HTTP_PORT=8080": "HTTP_PORT=80",
            "HTTPS_PORT=8443": "HTTPS_PORT=443",
        }.items():
            values = values.replace(previous, updated)
    try:
        descriptor = os.open(root / ".env", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        parser.exit(1, ".env já existe; não foi alterado.\n")
    with os.fdopen(descriptor, "w") as output:
        output.write(values)
    print(".env criado com secrets aleatórios e permissão 0600; valores não exibidos.")


if __name__ == "__main__":
    main()
