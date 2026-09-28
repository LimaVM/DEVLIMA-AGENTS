from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MemoryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str = Field(min_length=1, max_length=1000)
    category: Literal["preference", "fact"] = "fact"

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        from app.agent.memory_manager import safe_memory_content

        if not safe_memory_content(value):
            raise ValueError("Conteúdo vazio ou sensível não permitido como memória")
        return value.strip()


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    content: str
    category: str
    is_active: bool
    created_at: datetime


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
