from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ProviderName = Literal["llama_cpp", "groq"]


class LLMMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=8000)


class LLMCompletion(BaseModel):
    content: str = Field(min_length=1, max_length=131072)
    provider: ProviderName
    model: str
    upstream_request_id: str | None = None
    prompt_tokens: int | None = Field(default=None, ge=0)
    completion_tokens: int | None = Field(default=None, ge=0)


class ProviderHealth(BaseModel):
    provider: ProviderName
    configured: bool
    healthy: bool
    model: str
    latency_ms: int
    error_code: str | None = None


class LLMError(Exception):
    """Only stable error codes escape providers; upstream bodies/keys never do."""

    def __init__(self, code: str, *, status_code: int | None = None):
        super().__init__(code)
        self.code = code
        self.status_code = status_code

    @property
    def allows_fallback(self) -> bool:
        return self.code in {"timeout", "connection_error", "server_error", "model_unavailable"}


class LLMProvider(ABC):
    name: ProviderName
    model: str

    @abstractmethod
    def chat(
        self, messages: list[LLMMessage], *, max_tokens: int = 512, json_mode: bool = False
    ) -> LLMCompletion:
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> ProviderHealth:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
