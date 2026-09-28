import json
from datetime import UTC
from typing import Literal
from uuid import UUID

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from app.agent.errors import InvalidAgentResponse


# Documentação: Define o tipo StrictModel e reúne o estado/contrato descrito para este módulo.
class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# Documentação: Define o tipo TaskCreate e reúne o estado/contrato descrito para este módulo.
class TaskCreate(StrictModel):
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=2000)
    due_at: AwareDatetime | None = None


# Documentação: Define o tipo IdArguments e reúne o estado/contrato descrito para este módulo.
class IdArguments(StrictModel):
    id: UUID


# Documentação: Define o tipo TaskUpdate e reúne o estado/contrato descrito para este módulo.
class TaskUpdate(IdArguments):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=2000)
    due_at: AwareDatetime | None = None


# Documentação: Define o tipo ReminderCreate e reúne o estado/contrato descrito para este módulo.
class ReminderCreate(StrictModel):
    text: str = Field(min_length=1, max_length=1000)
    datetime: AwareDatetime
    rrule: str | None = Field(default=None, max_length=500)


# Documentação: Define o tipo ReminderUpdate e reúne o estado/contrato descrito para este módulo.
class ReminderUpdate(IdArguments):
    text: str | None = Field(default=None, min_length=1, max_length=1000)
    datetime: AwareDatetime | None = None


# Documentação: Define o tipo CallCreate e reúne o estado/contrato descrito para este módulo.
class CallCreate(StrictModel):
    datetime: AwareDatetime
    reason: str = Field(default="Conversar com o agente", max_length=500)
    rrule: str | None = Field(default=None, max_length=500)


# Documentação: Define o tipo ListArguments e reúne o estado/contrato descrito para este módulo.
class ListArguments(StrictModel):
    date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")


# Documentação: Define o tipo EmptyArguments e reúne o estado/contrato descrito para este módulo.
class EmptyArguments(StrictModel):
    pass


# Documentação: Define o tipo WorkerCreate e reúne o estado/contrato descrito para este módulo.
class WorkerCreate(StrictModel):
    name: str | None = Field(default=None, min_length=1, max_length=64, pattern=r"^[a-z0-9-]+$")
    vcpu: int = Field(default=2, ge=1, le=4)
    ram_mb: int = Field(default=2048, ge=512, le=8192)
    disk_gb: int = Field(default=20, ge=10, le=80)


# Documentação: Define o tipo WorkerArguments e reúne o estado/contrato descrito para este módulo.
class WorkerArguments(StrictModel):
    worker_id: UUID


# Documentação: Define o tipo WorkerRestore e reúne o estado/contrato descrito para este módulo.
class WorkerRestore(WorkerArguments):
    snapshot_id: UUID


# Documentação: Define o tipo WorkerJob e reúne o estado/contrato descrito para este módulo.
class WorkerJob(WorkerArguments):
    script: str = Field(min_length=1, max_length=8000)
    timeout: int = Field(default=120, ge=1, le=300)


ARGUMENT_SCHEMAS = {
    "create_task": TaskCreate,
    "update_task": TaskUpdate,
    "complete_task": IdArguments,
    "list_tasks": ListArguments,
    "create_reminder": ReminderCreate,
    "update_reminder": ReminderUpdate,
    "cancel_reminder": IdArguments,
    "list_reminders": ListArguments,
    "schedule_call": CallCreate,
    "cancel_call": IdArguments,
    "list_scheduled_calls": ListArguments,
    "create_linux_worker": WorkerCreate,
    "destroy_worker": WorkerArguments,
    "reset_worker": WorkerArguments,
    "snapshot_worker": WorkerArguments,
    "restore_worker": WorkerRestore,
    "get_worker_status": WorkerArguments,
    "list_workers": EmptyArguments,
    "start_worker": WorkerArguments,
    "stop_worker": WorkerArguments,
    "run_worker_job": WorkerJob,
}


# Documentação: Define o tipo ActionProposal e reúne o estado/contrato descrito para este módulo.
class ActionProposal(StrictModel):
    type: str
    arguments: dict

    @model_validator(mode="after")
    # Documentação: Confere argumentos contra o schema específico da ação antes do despacho.
    def validate_arguments(self):
        schema = ARGUMENT_SCHEMAS.get(self.type)
        if schema is None:
            raise ValueError("Ação não permitida")
        parsed = schema.model_validate(self.arguments)
        for name in ("due_at", "datetime"):
            value = getattr(parsed, name, None)
            if value is not None:
                setattr(parsed, name, value.astimezone(UTC))
        self.arguments = parsed.model_dump(mode="json", exclude_none=True)
        return self


# Documentação: Define o tipo MemoryProposal e reúne o estado/contrato descrito para este módulo.
class MemoryProposal(StrictModel):
    content: str = Field(min_length=1, max_length=1000)
    category: Literal["preference", "fact"]
    confidence: float = Field(ge=0, le=1)


# Documentação: Define o tipo AgentEnvelope e reúne o estado/contrato descrito para este módulo.
class AgentEnvelope(StrictModel):
    reply: str = Field(min_length=1, max_length=4000)
    actions: list[ActionProposal] = Field(default_factory=list, max_length=8)
    memory_candidates: list[MemoryProposal] = Field(default_factory=list, max_length=5)

    @field_validator("reply")
    @classmethod
    # Documentação: Implementa AgentEnvelope.not_blank como parte do fluxo descrito para este
    # arquivo.
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError("Resposta vazia")
        return value


# Documentação: Define o tipo SummaryEnvelope e reúne o estado/contrato descrito para este módulo.
class SummaryEnvelope(StrictModel):
    summary: str = Field(min_length=1, max_length=1800)
    facts: list[str] = Field(default_factory=list, max_length=8)
    open_topics: list[str] = Field(default_factory=list, max_length=8)

    @model_validator(mode="after")
    # Documentação: Implementa SummaryEnvelope.bound_items como parte do fluxo descrito para este
    # arquivo.
    def bound_items(self):
        if not self.summary.strip() or any(
            not item.strip() or len(item) > 160 for item in self.facts + self.open_topics
        ):
            raise ValueError("Resumo excede o limite")
        return self


# Documentação: Recusa objetos JSON que reutilizam a mesma chave, evitando interpretações
# divergentes.
def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Chave duplicada")
        result[key] = value
    return result


# Documentação: Valida envelope JSON estruturado da LLM e recusa resposta fora do contrato.
def parse_response(raw: str, schema=AgentEnvelope):
    try:
        if len(raw) > 20000:
            raise ValueError("Resposta muito grande")
        data = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
        return schema.model_validate(data)
    except (ValueError, TypeError, ValidationError, RecursionError):
        raise InvalidAgentResponse() from None
