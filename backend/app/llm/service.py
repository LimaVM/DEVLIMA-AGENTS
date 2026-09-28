from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.config import Settings
from app.llm.groq import GroqProvider
from app.llm.llama_cpp import LlamaCppProvider
from app.llm.router import LLMAttempt, LLMRouter
from app.models import AuditLog, LLMRequest


class DatabaseAuditRecorder:
    """Commits each attempt. Call before opening any action transaction."""

    def __init__(self, session: Session):
        self.session = session

    def __call__(self, attempt: LLMAttempt) -> None:
        completion = attempt.completion
        self.session.add(
            LLMRequest(
                request_id=attempt.request_id,
                user_id=attempt.user_id,
                provider=attempt.provider,
                model=attempt.model,
                latency_ms=attempt.latency_ms,
                success=attempt.success,
                fallback=attempt.fallback,
                error_code=attempt.error_code,
                status_code=attempt.status_code,
                upstream_request_id=completion.upstream_request_id if completion else None,
                prompt_tokens=completion.prompt_tokens if completion else None,
                completion_tokens=completion.completion_tokens if completion else None,
            )
        )
        self.session.add(
            AuditLog(
                user_id=attempt.user_id,
                event="llm.request",
                request_id=str(attempt.request_id),
                details={
                    "provider": attempt.provider,
                    "success": attempt.success,
                    "fallback": attempt.fallback,
                    "error_code": attempt.error_code,
                    "latency_ms": attempt.latency_ms,
                },
            )
        )
        self.session.commit()


@contextmanager
def build_router(settings: Settings, session: Session):
    router = LLMRouter(
        LlamaCppProvider(
            settings.local_llm_base_url,
            settings.local_llm_model,
            timeout=settings.local_llm_timeout,
            health_timeout=settings.llm_health_timeout,
        ),
        GroqProvider(
            settings.groq_model,
            api_key=settings.groq_api_key.get_secret_value(),
            timeout=settings.groq_timeout,
            health_timeout=settings.llm_health_timeout,
        ),
        allow_cloud_fallback=settings.allow_cloud_fallback,
        record_attempt=DatabaseAuditRecorder(session),
    )
    try:
        yield router
    finally:
        router.close()
