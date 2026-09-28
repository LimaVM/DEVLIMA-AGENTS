from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.core import AgentCore
from app.agent.errors import AgentError
from app.calls.service import CallService, state
from app.config import get_settings
from app.db.session import get_session
from app.llm.base import LLMError
from app.models import User
from app.models.calls import CallSession
from app.models.devices import RefreshFamily
from app.schemas.chat import ChatSend
from app.security import bearer, decode_token, get_current_user

router = APIRouter(prefix="/calls", tags=["calls"])


# Documentação: Define o tipo DeviceAction e reúne o estado/contrato descrito para este módulo.
class DeviceAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    device_id: UUID


# Documentação: Define o tipo Transcript e reúne o estado/contrato descrito para este módulo.
class Transcript(DeviceAction):
    client_message_id: UUID
    content: str = Field(min_length=1, max_length=4000)


# Documentação: Implementa bind como parte do fluxo descrito para este arquivo.
def bind(session, user, data, credentials):
    claims = decode_token(credentials.credentials, get_settings())
    if "sid" in claims:
        family = session.get(RefreshFamily, UUID(claims["sid"]))
        if family.device_id != data.device_id:
            raise HTTPException(403, "device_session_mismatch")
    return CallService(session, user.id, data.device_id)


@router.get("")
# Documentação: Lista list_calls, segundo o contrato e as verificações deste módulo.
def list_calls(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=100),
):
    CallService(session, user.id).expire()
    session.commit()
    return [
        state(row)
        for row in session.scalars(
            select(CallSession)
            .where(CallSession.user_id == user.id)
            .order_by(CallSession.started_at.desc())
            .limit(limit)
        )
    ]


@router.post("/incoming/{identifier}/{operation}")
# Documentação: Implementa incoming como parte do fluxo descrito para este arquivo.
def incoming(
    identifier: UUID,
    operation: str,
    data: DeviceAction,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    credentials=Depends(bearer),
):
    if operation not in {"answer", "reject"}:
        raise HTTPException(404, "not_found")
    try:
        service = bind(session, user, data, credentials)
        result = getattr(service, operation)(identifier)
        session.commit()
        return result
    except AgentError as error:
        session.rollback()
        raise HTTPException(error.status_code, error.code) from None


@router.post("/{identifier}/end")
# Documentação: Implementa end como parte do fluxo descrito para este arquivo.
def end(
    identifier: UUID,
    data: DeviceAction,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    credentials=Depends(bearer),
):
    try:
        result = bind(session, user, data, credentials).end(identifier)
        session.commit()
        return result
    except AgentError as error:
        session.rollback()
        raise HTTPException(error.status_code, error.code) from None


@router.post("/{identifier}/transcript")
# Documentação: Implementa transcript como parte do fluxo descrito para este arquivo.
def transcript(
    identifier: UUID,
    data: Transcript,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    credentials=Depends(bearer),
):
    try:
        conversation_id = bind(session, user, data, credentials).touch(identifier)
        session.commit()
        return AgentCore(session, get_settings()).send(
            user.id,
            ChatSend(
                conversation_id=conversation_id,
                client_message_id=data.client_message_id,
                content=data.content,
            ),
        )
    except (AgentError, LLMError) as error:
        session.rollback()
        raise HTTPException(getattr(error, "status_code", 503), error.code) from None
