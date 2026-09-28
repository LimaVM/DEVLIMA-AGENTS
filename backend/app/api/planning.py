from datetime import date, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.agent.action_parser import CallCreate, ReminderCreate, TaskCreate
from app.agent.errors import AgentError
from app.db.session import get_session
from app.models import User
from app.planning.service import PlanningService
from app.security import get_current_user

router = APIRouter(tags=["planning"])


# Documentação: Define o tipo TaskPatch e reúne o estado/contrato descrito para este módulo.
class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(None, min_length=1, max_length=300)
    description: str | None = Field(None, max_length=2000)
    due_at: AwareDatetime | None = None


# Documentação: Define o tipo ReminderPatch e reúne o estado/contrato descrito para este módulo.
class ReminderPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = Field(None, min_length=1, max_length=1000)
    datetime: AwareDatetime | None = None
    rrule: str | None = Field(None, max_length=500)


# Documentação: Define o tipo TaskResponse e reúne o estado/contrato descrito para este módulo.
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str | None
    due_at: datetime | None
    status: str
    created_at: datetime
    updated_at: datetime


# Documentação: Define o tipo ScheduleResponse e reúne o estado/contrato descrito para este
# módulo.
class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    kind: str
    text: str
    timezone: str
    start_at: datetime
    next_run_at: datetime | None
    rrule: str | None
    status: str
    version: int
    created_at: datetime


# Documentação: Implementa invoke como parte do fluxo descrito para este arquivo.
def invoke(session, user, operation, *args):
    try:
        result = getattr(PlanningService(session, user.id), operation)(*args)
        session.commit()
        return result
    except AgentError as error:
        session.rollback()
        raise HTTPException(error.status_code, error.code) from None


@router.post("/tasks", response_model=TaskResponse, status_code=201)
# Documentação: Cria create_task, segundo o contrato e as verificações deste módulo.
def create_task(
    data: TaskCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "create_task", data.model_dump())


@router.get("/tasks", response_model=list[TaskResponse])
# Documentação: Lista list_tasks, segundo o contrato e as verificações deste módulo.
def list_tasks(
    day: date | None = Query(None, alias="date"),
    status: str | None = Query(None, pattern="^(OPEN|COMPLETED)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "list_tasks", day, status, limit, offset)


@router.patch("/tasks/{identifier}", response_model=TaskResponse)
# Documentação: Atualiza update_task, segundo o contrato e as verificações deste módulo.
def update_task(
    identifier: UUID,
    data: TaskPatch,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "update_task", identifier, data.model_dump(exclude_unset=True))


@router.post("/tasks/{identifier}/complete", response_model=TaskResponse)
# Documentação: Implementa complete_task como parte do fluxo descrito para este arquivo.
def complete_task(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "complete_task", identifier)


@router.post("/reminders", response_model=ScheduleResponse, status_code=201)
# Documentação: Cria create_reminder, segundo o contrato e as verificações deste módulo.
def create_reminder(
    data: ReminderCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "create_schedule", "REMINDER", data.model_dump())


@router.get("/reminders", response_model=list[ScheduleResponse])
# Documentação: Lista list_reminders, segundo o contrato e as verificações deste módulo.
def list_reminders(
    day: date | None = Query(None, alias="date"),
    status: str | None = Query(None, pattern="^(SCHEDULED|CANCELLED|COMPLETED)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "list_schedules", "REMINDER", day, status, limit, offset)


@router.patch("/reminders/{identifier}", response_model=ScheduleResponse)
# Documentação: Atualiza update_reminder, segundo o contrato e as verificações deste módulo.
def update_reminder(
    identifier: UUID,
    data: ReminderPatch,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "update_schedule", identifier, data.model_dump(exclude_unset=True))


@router.delete("/reminders/{identifier}", response_model=ScheduleResponse)
# Documentação: Cancela cancel_reminder, segundo o contrato e as verificações deste módulo.
def cancel_reminder(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "cancel_schedule", identifier, "REMINDER")


@router.post("/scheduled-calls", response_model=ScheduleResponse, status_code=201)
# Documentação: Cria create_call, segundo o contrato e as verificações deste módulo.
def create_call(
    data: CallCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "create_schedule", "CALL", data.model_dump())


@router.get("/scheduled-calls", response_model=list[ScheduleResponse])
# Documentação: Lista list_calls, segundo o contrato e as verificações deste módulo.
def list_calls(
    day: date | None = Query(None, alias="date"),
    status: str | None = Query(None, pattern="^(SCHEDULED|CANCELLED|COMPLETED)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "list_schedules", "CALL", day, status, limit, offset)


@router.delete("/scheduled-calls/{identifier}", response_model=ScheduleResponse)
# Documentação: Cancela cancel_call, segundo o contrato e as verificações deste módulo.
def cancel_call(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "cancel_schedule", identifier, "CALL")
