"""Streaming, authenticated AES-256-GCM backup envelope. Keys are external binary files."""

import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MAGIC = b"DLAGBACKUP1"


def secret(path):
    path = Path(path)
    if path.stat().st_mode & 0o077:
        raise ValueError("Backup key must have mode 0600")
    key = path.read_bytes()
    if len(key) != 32:
        raise ValueError("Backup key must be exactly 32 bytes")
    return key


def encrypt(source, target, key_path):
    nonce = os.urandom(12)
    encryptor = Cipher(algorithms.AES(secret(key_path)), modes.GCM(nonce)).encryptor()
    header = MAGIC + nonce
    encryptor.authenticate_additional_data(header)
    with open(source, "rb") as input_file, open(target, "xb") as output:
        os.chmod(target, 0o600)
        output.write(header)
        while block := input_file.read(1024 * 1024):
            output.write(encryptor.update(block))
        output.write(encryptor.finalize())
        output.write(encryptor.tag)


def decrypt(source, target, key_path):
    with open(source, "rb") as input_file:
        header = input_file.read(len(MAGIC) + 12)
        if not header.startswith(MAGIC):
            raise ValueError("Invalid backup envelope")
        input_file.seek(-16, 2)
        tag = input_file.read(16)
        remaining = input_file.tell() - 16 - len(header)
        if remaining < 0:
            raise ValueError("Truncated backup")
        input_file.seek(len(header))
        decryptor = Cipher(
            algorithms.AES(secret(key_path)), modes.GCM(header[len(MAGIC) :], tag)
        ).decryptor()
        decryptor.authenticate_additional_data(header)
        created = False
        try:
            with open(target, "xb") as output:
                created = True
                os.chmod(target, 0o600)
                while remaining:
                    block = input_file.read(min(1024 * 1024, remaining))
                    if not block:
                        raise ValueError("Truncated backup")
                    remaining -= len(block)
                    output.write(decryptor.update(block))
                output.write(decryptor.finalize())
        except Exception:
            if created:
                Path(target).unlink(missing_ok=True)
            raise


def sha256(path):
    import hashlib

    digest = hashlib.sha256()
    with open(path, "rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()
