from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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
