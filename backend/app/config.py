from functools import lru_cache
from ipaddress import ip_address, ip_network
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", hide_input_in_errors=True)

    app_name: str = "DEVLIMA AGENT"
    app_environment: str = "production"
    enable_api_docs: bool = False
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "devlima_agent"
    postgres_user: str = "agent"
    postgres_password: SecretStr
    jwt_secret: SecretStr
    jwt_issuer: str = "devlima-agent"
    jwt_audience: str = "devlima-android"
    jwt_ttl_minutes: int = 30
    default_timezone: str = "America/Sao_Paulo"
    login_max_attempts: int = 5
    login_window_seconds: int = 900
    local_llm_base_url: str = ""
    local_llm_model: str = ""
    local_llm_timeout: float = 30
    groq_api_key: SecretStr = SecretStr("")
    groq_model: str = "openai/gpt-oss-120b"
    groq_timeout: float = 30
    llm_health_timeout: float = 5
    allow_cloud_fallback: bool = True
    scheduler_poll_seconds: int = 5
    context_recent_messages: int = 8
    context_max_chars: int = 12000
    summary_trigger_messages: int = 16

    @model_validator(mode="after")
    def validate_context_limits(self):
        if not 1 <= self.scheduler_poll_seconds <= 60:
            raise ValueError("Scheduler poll deve ser entre 1 e 60 segundos")
        if not 2 <= self.context_recent_messages <= 16:
            raise ValueError("Janela de contexto deve ter entre 2 e 16 mensagens")
        if not 10000 <= self.context_max_chars <= 16000:
            raise ValueError("Contexto deve ter entre 10000 e 16000 caracteres")
        if not self.context_recent_messages < self.summary_trigger_messages <= 100:
            raise ValueError("Trigger de resumo deve exceder a janela recente e ser até 100")
        return self

    @field_validator("local_llm_base_url")
    @classmethod
    def validate_local_url(cls, value: str) -> str:
        if not value:
            return value
        parsed = urlsplit(value)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("LOCAL_LLM_BASE_URL deve ser uma URL privada sem credenciais")
        try:
            if parsed.port is not None and not 1 <= parsed.port <= 65535:
                raise ValueError("Porta inválida")
        except ValueError:
            raise ValueError("Porta da LLM inválida") from None
        try:
            address = ip_address(parsed.hostname)
        except ValueError:
            if parsed.hostname != "localhost" and not parsed.hostname.endswith(".ts.net"):
                raise ValueError(
                    "Use IP privado, localhost ou hostname Tailscale .ts.net"
                ) from None
        else:
            private_networks = (
                "10.0.0.0/8",
                "172.16.0.0/12",
                "192.168.0.0/16",
                "100.64.0.0/10",
                "127.0.0.0/8",
                "::1/128",
                "fc00::/7",
            )
            if not any(address in ip_network(network) for network in private_networks):
                raise ValueError("A LLM primária deve usar endereço privado")
        return value.rstrip("/")

    @field_validator("local_llm_timeout", "groq_timeout", "llm_health_timeout")
    @classmethod
    def validate_timeout(cls, value: float) -> float:
        if not 0 < value <= 120:
            raise ValueError("Timeout deve estar entre 0 e 120 segundos")
        return value

    @field_validator("local_llm_model", "groq_model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        if len(value) > 512 or "\n" in value or "\r" in value:
            raise ValueError("Identificador de modelo inválido")
        return value

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt_secret(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < 32:
            raise ValueError("JWT_SECRET deve ter pelo menos 32 caracteres")
        return value

    @field_validator("postgres_password")
    @classmethod
    def validate_db_password(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < 16:
            raise ValueError("POSTGRES_PASSWORD deve ter pelo menos 16 caracteres")
        return value

    @field_validator("default_timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Timezone IANA inválido") from exc
        return value

    @field_validator("jwt_ttl_minutes", "login_max_attempts", "login_window_seconds")
    @classmethod
    def validate_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Valor deve ser positivo")
        return value

    @property
    def database_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
