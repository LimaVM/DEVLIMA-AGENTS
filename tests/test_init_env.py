import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EnvironmentGenerationTests(unittest.TestCase):
    def layout(self, folder):
        root = Path(folder)
        (root / "scripts").mkdir()
        shutil.copy(ROOT / "scripts/init_env.py", root / "scripts/init_env.py")
        shutil.copy(ROOT / ".env.example", root / ".env.example")
        return root

    def test_role_passwords_are_distinct_private_and_existing_env_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self.layout(folder)
            script = root / "scripts/init_env.py"
            result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            original = (root / ".env").read_bytes()
            values = dict(
                line.split("=", 1)
                for line in original.decode().splitlines()
                if line and not line.startswith("#") and "=" in line
            )
            passwords = [
                values[key]
                for key in (
                    "POSTGRES_PASSWORD",
                    "RUNTIME_POSTGRES_PASSWORD",
                    "MIGRATION_POSTGRES_PASSWORD",
                )
            ]
            self.assertEqual(len(set(passwords)), 3)
            self.assertTrue(all(len(p) >= 32 for p in passwords))
            self.assertEqual((root / ".env").stat().st_mode & 0o777, 0o600)
            self.assertFalse(any(password in result.stdout for password in passwords))
            repeated = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertEqual((root / ".env").read_bytes(), original)

    def test_domain_configuration_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self.layout(folder)
            script = root / "scripts/init_env.py"
            result = subprocess.run(
                [sys.executable, str(script), "--domain", "invalid;hostname"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / ".env").exists())
            result = subprocess.run(
                [sys.executable, str(script), "--domain", "agent.example.com"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            values = (root / ".env").read_text()
            self.assertIn("AGENT_DOMAIN=agent.example.com", values)
            self.assertIn("CADDY_BIND=0.0.0.0", values)


if __name__ == "__main__":
    unittest.main()
