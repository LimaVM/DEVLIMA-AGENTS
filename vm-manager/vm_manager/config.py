from pathlib import Path

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VM_MANAGER_", hide_input_in_errors=True)
    token: SecretStr
    state_root: Path = Path("/var/lib/devlima-vm-manager")
    worker_root: Path = Path("/var/lib/libvirt/images/devlima-workers")
    template: Path = Path("/var/lib/libvirt/images/templates/ubuntu-24.04-base.qcow2")
    template_sha256: str = "6a81c37564db9b1ee84e141922625e1d7c5b389b99bb3c572e0243607d5bb4d2"
    ssh_private_key: Path = Path("/root/.ssh/agent_worker")
    ssh_public_key: Path = Path("/root/.ssh/agent_worker.pub")
    max_workers: int = 2
    max_total_vcpu: int = 4
    max_total_ram_mb: int = 8192
    host_ram_reserve_mb: int = 4096
    disk_reserve_gb: int = 10
    network: str = "default"

    @field_validator("token")
    @classmethod
    def secure_token(cls, value):
        if len(value.get_secret_value()) < 32:
            raise ValueError("Manager token must have at least 32 characters")
        return value


class VMError(Exception):
    def __init__(self, code, status=409):
        self.code, self.status = code, status
        super().__init__(code)
