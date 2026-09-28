from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ProviderName = Literal["llama_cpp", "groq"]


# Documentação: Define o tipo LLMMessage e reúne o estado/contrato descrito para este módulo.
class LLMMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=8000)


# Documentação: Define o tipo LLMCompletion e reúne o estado/contrato descrito para este módulo.
class LLMCompletion(BaseModel):
    content: str = Field(min_length=1, max_length=131072)
    provider: ProviderName
    model: str
    upstream_request_id: str | None = None
    prompt_tokens: int | None = Field(default=None, ge=0)
    completion_tokens: int | None = Field(default=None, ge=0)


# Documentação: Define o tipo ProviderHealth e reúne o estado/contrato descrito para este módulo.
class ProviderHealth(BaseModel):
    provider: ProviderName
    configured: bool
    healthy: bool
    model: str
    latency_ms: int
    error_code: str | None = None


# Documentação: Define o tipo LLMError e reúne o estado/contrato descrito para este módulo.
class LLMError(Exception):
    """Only stable error codes escape providers; upstream bodies/keys never do."""

    # Documentação: Inicializa LLMError com as dependências e estado declarados.
    def __init__(self, code: str, *, status_code: int | None = None):
        super().__init__(code)
        self.code = code
        self.status_code = status_code

    @property
    # Documentação: Implementa LLMError.allows_fallback como parte do fluxo descrito para este
    # arquivo.
    def allows_fallback(self) -> bool:
        return self.code in {"timeout", "connection_error", "server_error", "model_unavailable"}


# Documentação: Define o tipo LLMProvider e reúne o estado/contrato descrito para este módulo.
class LLMProvider(ABC):
    name: ProviderName
    model: str

    @abstractmethod
    # Documentação: Implementa LLMProvider.chat como parte do fluxo descrito para este arquivo.
    def chat(
        self, messages: list[LLMMessage], *, max_tokens: int = 512, json_mode: bool = False
    ) -> LLMCompletion:
        raise NotImplementedError

    @abstractmethod
    # Documentação: Implementa LLMProvider.health_check como parte do fluxo descrito para este
    # arquivo.
    def health_check(self) -> ProviderHealth:
        raise NotImplementedError

    @abstractmethod
    # Documentação: Libera LLMProvider.close, segundo o contrato e as verificações deste módulo.
    def close(self) -> None:
        raise NotImplementedError
