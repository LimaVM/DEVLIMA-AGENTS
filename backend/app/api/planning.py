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


class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(None, min_length=1, max_length=300)
    description: str | None = Field(None, max_length=2000)
    due_at: AwareDatetime | None = None


class ReminderPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = Field(None, min_length=1, max_length=1000)
    datetime: AwareDatetime | None = None
    rrule: str | None = Field(None, max_length=500)


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str | None
    due_at: datetime | None
    status: str
    created_at: datetime
    updated_at: datetime


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


def invoke(session, user, operation, *args):
    try:
        result = getattr(PlanningService(session, user.id), operation)(*args)
        session.commit()
        return result
    except AgentError as error:
        session.rollback()
        raise HTTPException(error.status_code, error.code) from None


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    data: TaskCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "create_task", data.model_dump())


@router.get("/tasks", response_model=list[TaskResponse])
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
def update_task(
    identifier: UUID,
    data: TaskPatch,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "update_task", identifier, data.model_dump(exclude_unset=True))


@router.post("/tasks/{identifier}/complete", response_model=TaskResponse)
def complete_task(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "complete_task", identifier)


@router.post("/reminders", response_model=ScheduleResponse, status_code=201)
def create_reminder(
    data: ReminderCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "create_schedule", "REMINDER", data.model_dump())


@router.get("/reminders", response_model=list[ScheduleResponse])
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
def update_reminder(
    identifier: UUID,
    data: ReminderPatch,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "update_schedule", identifier, data.model_dump(exclude_unset=True))


@router.delete("/reminders/{identifier}", response_model=ScheduleResponse)
def cancel_reminder(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "cancel_schedule", identifier, "REMINDER")


@router.post("/scheduled-calls", response_model=ScheduleResponse, status_code=201)
def create_call(
    data: CallCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "create_schedule", "CALL", data.model_dump())


@router.get("/scheduled-calls", response_model=list[ScheduleResponse])
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
def cancel_call(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return invoke(session, user, "cancel_schedule", identifier, "CALL")
