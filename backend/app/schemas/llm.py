from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.llm.base import LLMMessage, ProviderName


class LLMChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    messages: list[LLMMessage] = Field(min_length=1, max_length=32)
    max_tokens: int = Field(default=512, ge=1, le=2048)

    @model_validator(mode="after")
    def bound_context(self):
        if sum(len(message.content) for message in self.messages) > 16000:
            raise ValueError("Contexto excede o limite de 16000 caracteres")
        if not any(message.role == "user" for message in self.messages):
            raise ValueError("É necessária ao menos uma mensagem do usuário")
        return self


class LLMChatResponse(BaseModel):
    request_id: UUID
    reply: str
    provider: ProviderName
    model: str
    fallback_used: bool
    latency_ms: int
