from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter
from uuid import UUID, uuid4

from app.llm.base import LLMCompletion, LLMError, LLMMessage, LLMProvider, ProviderName


@dataclass(frozen=True)
# Documentação: Define o tipo LLMAttempt e reúne o estado/contrato descrito para este módulo.
class LLMAttempt:
    request_id: UUID
    user_id: UUID | None
    provider: ProviderName
    model: str
    latency_ms: int
    success: bool
    fallback: bool
    error_code: str | None = None
    status_code: int | None = None
    completion: LLMCompletion | None = None


@dataclass(frozen=True)
# Documentação: Define o tipo RoutedCompletion e reúne o estado/contrato descrito para este
# módulo.
class RoutedCompletion:
    request_id: UUID
    completion: LLMCompletion
    fallback_used: bool
    latency_ms: int


# Documentação: Define o tipo LLMRouter e reúne o estado/contrato descrito para este módulo.
class LLMRouter:
    # Documentação: Inicializa LLMRouter com as dependências e estado declarados.
    def __init__(
        self,
        local: LLMProvider,
        cloud: LLMProvider,
        *,
        allow_cloud_fallback: bool,
        record_attempt: Callable[[LLMAttempt], None],
    ):
        self.local = local
        self.cloud = cloud
        self.allow_cloud_fallback = allow_cloud_fallback
        self.record_attempt = record_attempt

    # Documentação: Implementa LLMRouter._chat como parte do fluxo descrito para este arquivo.
    def _chat(
        self,
        provider: LLMProvider,
        messages: list[LLMMessage],
        *,
        request_id: UUID,
        user_id: UUID | None,
        fallback: bool,
        max_tokens: int,
        json_mode: bool,
    ) -> LLMCompletion:
        started = perf_counter()
        try:
            completion = provider.chat(messages, max_tokens=max_tokens, json_mode=json_mode)
        except LLMError as error:
            self.record_attempt(
                LLMAttempt(
                    request_id=request_id,
                    user_id=user_id,
                    provider=provider.name,
                    model=provider.model,
                    latency_ms=max(0, round((perf_counter() - started) * 1000)),
                    success=False,
                    fallback=fallback,
                    error_code=error.code,
                    status_code=error.status_code,
                )
            )
            raise
        self.record_attempt(
            LLMAttempt(
                request_id=request_id,
                user_id=user_id,
                provider=provider.name,
                model=provider.model,
                latency_ms=max(0, round((perf_counter() - started) * 1000)),
                success=True,
                fallback=fallback,
                completion=completion,
            )
        )
        return completion

    # Documentação: Tenta provider primário, avalia elegibilidade de fallback e retorna resultado
    # com auditoria de tentativas.
    def chat(
        self,
        messages: list[LLMMessage],
        *,
        max_tokens: int = 512,
        json_mode: bool = False,
        request_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> RoutedCompletion:
        correlation = request_id or uuid4()
        started = perf_counter()
        used_fallback = False
        try:
            completion = self._chat(
                self.local,
                messages,
                request_id=correlation,
                user_id=user_id,
                fallback=False,
                max_tokens=max_tokens,
                json_mode=json_mode,
            )
        except LLMError as error:
            if not self.allow_cloud_fallback or not error.allows_fallback:
                raise
            used_fallback = True
            completion = self._chat(
                self.cloud,
                messages,
                request_id=correlation,
                user_id=user_id,
                fallback=True,
                max_tokens=max_tokens,
                json_mode=json_mode,
            )
        return RoutedCompletion(
            request_id=correlation,
            completion=completion,
            fallback_used=used_fallback,
            latency_ms=max(0, round((perf_counter() - started) * 1000)),
        )

    # Documentação: Implementa LLMRouter.health_check como parte do fluxo descrito para este
    # arquivo.
    def health_check(self) -> dict:
        local = self.local.health_check().model_dump()
        if self.allow_cloud_fallback:
            cloud = self.cloud.health_check().model_dump()
        else:
            cloud = {"provider": self.cloud.name, "healthy": False, "error_code": "disabled"}
        return {"local": local, "cloud": cloud, "allow_cloud_fallback": self.allow_cloud_fallback}

    # Documentação: Libera LLMRouter.close, segundo o contrato e as verificações deste módulo.
    def close(self) -> None:
        self.local.close()
        self.cloud.close()
