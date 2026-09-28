from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Documentação: Define o tipo ConversationCreate e reúne o estado/contrato descrito para este
# módulo.
class ConversationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(default="Nova conversa", min_length=1, max_length=100)


# Documentação: Define o tipo ConversationResponse e reúne o estado/contrato descrito para este
# módulo.
class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    archived: bool
    created_at: datetime
    updated_at: datetime


# Documentação: Define o tipo MessageResponse e reúne o estado/contrato descrito para este módulo.
class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    conversation_id: UUID
    sequence: int
    role: str
    content: str
    status: str
    error_code: str | None
    created_at: datetime


# Documentação: Define o tipo ChatSend e reúne o estado/contrato descrito para este módulo.
class ChatSend(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conversation_id: UUID | None = None
    client_message_id: UUID
    content: str = Field(min_length=1, max_length=4000)

    @field_validator("content")
    @classmethod
    # Documentação: Implementa ChatSend.not_blank como parte do fluxo descrito para este arquivo.
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError("Mensagem vazia")
        return value


# Documentação: Define o tipo ChatReply e reúne o estado/contrato descrito para este módulo.
class ChatReply(BaseModel):
    conversation_id: UUID
    user_message_id: UUID
    assistant_message_id: UUID
    request_id: UUID
    reply: str
    provider: str
    fallback_used: bool
    latency_ms: int
    memory_candidates: list[dict]
    actions: list[dict]
    context_stats: dict
    replayed: bool = False


# Documentação: Define o tipo SummaryResponse e reúne o estado/contrato descrito para este módulo.
class SummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    through_sequence: int
    content: dict
    created_at: datetime
