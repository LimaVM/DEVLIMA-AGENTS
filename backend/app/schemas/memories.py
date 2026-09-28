from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Documentação: Define o tipo MemoryCreate e reúne o estado/contrato descrito para este módulo.
class MemoryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str = Field(min_length=1, max_length=1000)
    category: Literal["preference", "fact"] = "fact"

    @field_validator("content")
    @classmethod
    # Documentação: Valida MemoryCreate.validate_content, segundo o contrato e as verificações
    # deste módulo.
    def validate_content(cls, value):
        from app.agent.memory_manager import safe_memory_content

        if not safe_memory_content(value):
            raise ValueError("Conteúdo vazio ou sensível não permitido como memória")
        return value.strip()


# Documentação: Define o tipo MemoryResponse e reúne o estado/contrato descrito para este módulo.
class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    content: str
    category: str
    is_active: bool
    created_at: datetime


# Documentação: Define o tipo CandidateResponse e reúne o estado/contrato descrito para este
# módulo.
class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    content: str
    category: str
    confidence: float
    status: str
    rejection_reason: str | None
    accepted_memory_id: UUID | None
    created_at: datetime
