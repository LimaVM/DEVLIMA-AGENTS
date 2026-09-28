from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.core import AgentCore
from app.agent.errors import AgentError
from app.config import get_settings
from app.db.session import get_session
from app.llm.base import LLMError
from app.models import AuditLog, Conversation, ConversationSummary, Message, User
from app.schemas.chat import (
    ChatReply,
    ChatSend,
    ConversationCreate,
    ConversationResponse,
    MessageResponse,
    SummaryResponse,
)
from app.security import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


# Documentação: Implementa owned como parte do fluxo descrito para este arquivo.
def owned(session, user, identifier, lock=False):
    query = select(Conversation).where(
        Conversation.id == identifier, Conversation.user_id == user.id
    )
    row = session.scalar(query.with_for_update() if lock else query)
    if row is None:
        raise HTTPException(404, "not_found")
    return row


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
# Documentação: Cria create_conversation, segundo o contrato e as verificações deste módulo.
def create_conversation(
    data: ConversationCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    row = Conversation(user_id=user.id, title=data.title)
    session.add(row)
    session.flush()
    session.add(
        AuditLog(
            user_id=user.id, event="conversation.created", details={"conversation_id": str(row.id)}
        )
    )
    session.commit()
    return row


@router.get("/conversations", response_model=list[ConversationResponse])
# Documentação: Lista list_conversations, segundo o contrato e as verificações deste módulo.
def list_conversations(
    archived: bool = False,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.scalars(
        select(Conversation)
        .where(Conversation.user_id == user.id, Conversation.archived == archived)
        .order_by(Conversation.updated_at.desc(), Conversation.id)
        .offset(offset)
        .limit(limit)
    ).all()


@router.get("/conversations/{identifier}", response_model=ConversationResponse)
# Documentação: Obtém get_conversation, segundo o contrato e as verificações deste módulo.
def get_conversation(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return owned(session, user, identifier)


@router.post("/conversations/{identifier}/archive", status_code=204)
# Documentação: Implementa archive_conversation como parte do fluxo descrito para este arquivo.
def archive_conversation(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    row = owned(session, user, identifier, lock=True)
    if row.lease_owner and row.lease_until > datetime.now(UTC):
        raise HTTPException(409, "conversation_busy")
    if row.pending_message_id:
        source = session.get(Message, row.pending_message_id)
        source.status, source.error_code = "FAILED", "processing_lease_expired"
    row.lease_owner = row.lease_until = row.pending_message_id = None
    row.archived = True
    row.updated_at = datetime.now(UTC)
    session.add(
        AuditLog(
            user_id=user.id, event="conversation.archived", details={"conversation_id": str(row.id)}
        )
    )
    session.commit()
    return Response(status_code=204)


@router.get("/conversations/{identifier}/messages", response_model=list[MessageResponse])
# Documentação: Lista list_messages, segundo o contrato e as verificações deste módulo.
def list_messages(
    identifier: UUID,
    after_sequence: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    owned(session, user, identifier)
    return session.scalars(
        select(Message)
        .where(
            Message.conversation_id == identifier,
            Message.user_id == user.id,
            Message.sequence > after_sequence,
        )
        .order_by(Message.sequence)
        .limit(limit)
    ).all()


@router.get("/conversations/{identifier}/summaries", response_model=list[SummaryResponse])
# Documentação: Lista list_summaries, segundo o contrato e as verificações deste módulo.
def list_summaries(
    identifier: UUID,
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    owned(session, user, identifier)
    return session.scalars(
        select(ConversationSummary)
        .where(
            ConversationSummary.conversation_id == identifier,
            ConversationSummary.user_id == user.id,
        )
        .order_by(ConversationSummary.through_sequence.desc())
        .limit(limit)
    ).all()


@router.post("/messages", response_model=ChatReply)
# Documentação: Implementa send_message como parte do fluxo descrito para este arquivo.
def send_message(
    data: ChatSend, user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    try:
        return AgentCore(session, get_settings()).send(user.id, data)
    except AgentError as error:
        raise HTTPException(error.status_code, error.code) from None
    except LLMError as error:
        raise HTTPException(503, error.code) from None
