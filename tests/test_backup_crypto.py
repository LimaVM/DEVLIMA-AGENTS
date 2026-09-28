import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

from cryptography.exceptions import InvalidTag

spec = importlib.util.spec_from_file_location(
    "backup_crypto", Path(__file__).resolve().parents[1] / "scripts/backup_crypto.py"
)
crypto = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crypto)


# Documentação: Define o tipo BackupCryptoTests e reúne o estado/contrato descrito para este
# módulo.
class BackupCryptoTests(unittest.TestCase):
    # Documentação: Verifica o cenário
    # test_streaming_roundtrip_and_tampering_never_leaves_plaintext; as condições e resultados
    # esperados aparecem nos asserts.
    def test_streaming_roundtrip_and_tampering_never_leaves_plaintext(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            key = root / "key"
            key.write_bytes(os.urandom(32))
            key.chmod(0o600)
            original = root / "original"
            original.write_bytes(os.urandom(3 * 1024 * 1024 + 57))
            encrypted = root / "encrypted"
            crypto.encrypt(original, encrypted, key)
            restored = root / "restored"
            crypto.decrypt(encrypted, restored, key)
            self.assertEqual(crypto.sha256(original), crypto.sha256(restored))
            self.assertEqual(restored.stat().st_mode & 0o777, 0o600)
            damaged = bytearray(encrypted.read_bytes())
            damaged[len(crypto.MAGIC) + 100] ^= 1
            corrupt = root / "corrupt"
            corrupt.write_bytes(damaged)
            rejected = root / "rejected"
            with self.assertRaises(InvalidTag):
                crypto.decrypt(corrupt, rejected, key)
            self.assertFalse(rejected.exists())
            existing = root / "existing"
            existing.write_text("must remain")
            with self.assertRaises(FileExistsError):
                crypto.decrypt(encrypted, existing, key)
            self.assertEqual(existing.read_text(), "must remain")

    # Documentação: Verifica o cenário test_wrong_key_and_header_are_rejected; as condições e
    # resultados esperados aparecem nos asserts.
    def test_wrong_key_and_header_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("a", "b"):
                (root / name).write_bytes(os.urandom(32))
                (root / name).chmod(0o600)
            source = root / "source"
            source.write_bytes(b"private information")
            encrypted = root / "encrypted"
            crypto.encrypt(source, encrypted, root / "a")
            with self.assertRaises(InvalidTag):
                crypto.decrypt(encrypted, root / "bad", root / "b")
            self.assertFalse((root / "bad").exists())
            blob = bytearray(encrypted.read_bytes())
            blob[0] ^= 1
            encrypted.write_bytes(blob)
            with self.assertRaises(ValueError):
                crypto.decrypt(encrypted, root / "bad", root / "a")
            self.assertFalse((root / "bad").exists())

    # Documentação: Verifica o cenário test_public_key_file_permissions_and_length_are_refused; as
    # condições e resultados esperados aparecem nos asserts.
    def test_public_key_file_permissions_and_length_are_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            key = Path(temporary) / "key"
            key.write_bytes(os.urandom(32))
            key.chmod(0o644)
            with self.assertRaises(ValueError):
                crypto.secret(key)
            key.chmod(0o600)
            key.write_bytes(b"short")
            with self.assertRaises(ValueError):
                crypto.secret(key)


if __name__ == "__main__":
    unittest.main()
