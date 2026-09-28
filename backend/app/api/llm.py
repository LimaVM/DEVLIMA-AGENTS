from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db.session import get_session
from app.llm.base import LLMError
from app.llm.service import build_router
from app.models import User
from app.schemas.llm import LLMChatRequest, LLMChatResponse
from app.security import get_current_user

router = APIRouter(prefix="/llm", tags=["llm"])


@router.get("/health")
# Documentação: Implementa health como parte do fluxo descrito para este arquivo.
def health(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    with build_router(settings, session) as llm:
        return llm.health_check()


@router.post("/chat", response_model=LLMChatResponse)
# Documentação: Implementa chat como parte do fluxo descrito para este arquivo.
def chat(
    data: LLMChatRequest,
    request: Request,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> LLMChatResponse:
    try:
        with build_router(settings, session) as llm:
            result = llm.chat(
                data.messages,
                max_tokens=data.max_tokens,
                request_id=UUID(request.state.request_id),
                user_id=user.id,
            )
    except LLMError as error:
        raise HTTPException(status_code=503, detail={"code": error.code}) from None
    return LLMChatResponse(
        request_id=result.request_id,
        reply=result.completion.content,
        provider=result.completion.provider,
        model=result.completion.model,
        fallback_used=result.fallback_used,
        latency_ms=result.latency_ms,
    )
