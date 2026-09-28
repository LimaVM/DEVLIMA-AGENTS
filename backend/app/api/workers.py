from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field, model_validator
from sqlalchemy.orm import Session

from app.agent.action_parser import StrictModel, WorkerCreate
from app.agent.errors import AgentError
from app.db.session import get_session
from app.models import User
from app.security import get_current_user
from app.workers.service import WorkerService, command_data, snapshot_data, worker_data

router = APIRouter(prefix="/workers", tags=["workers"])


# Documentação: Define o tipo CreateRequest e reúne o estado/contrato descrito para este módulo.
class CreateRequest(WorkerCreate):
    request_id: UUID


# Documentação: Define o tipo CommandRequest e reúne o estado/contrato descrito para este módulo.
class CommandRequest(StrictModel):
    request_id: UUID
    kind: Literal["DESTROY", "RESET", "START", "STOP", "SNAPSHOT", "RESTORE", "EXECUTE"]
    snapshot_id: UUID | None = None
    script: str | None = Field(None, min_length=1, max_length=8000)
    timeout: int = Field(120, ge=1, le=300)

    @model_validator(mode="after")
    # Documentação: Valida CommandRequest.validate_operation, segundo o contrato e as verificações
    # deste módulo.
    def validate_operation(self):
        if self.kind == "RESTORE" and self.snapshot_id is None:
            raise ValueError("snapshot_id required")
        if self.kind != "RESTORE" and self.snapshot_id is not None:
            raise ValueError("snapshot_id only allowed for restore")
        if self.kind == "EXECUTE" and (not self.script or not self.script.strip()):
            raise ValueError("script required")
        if self.kind != "EXECUTE" and self.script is not None:
            raise ValueError("script only allowed for worker execution")
        return self


# Documentação: Implementa invoke como parte do fluxo descrito para este arquivo.
def invoke(session, owner, operation):
    try:
        data = operation(WorkerService(session, owner))
        session.commit()
        return data
    except AgentError as error:
        session.rollback()
        raise HTTPException(error.status_code, error.code) from None


@router.post("", status_code=202)
# Documentação: Cria create, segundo o contrato e as verificações deste módulo.
def create(
    data: CreateRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return invoke(
        session,
        user.id,
        lambda service: command_data(
            service.queue(
                "CREATE",
                data.model_dump(mode="json", exclude={"request_id"}, exclude_none=True),
                data.request_id,
            )
        ),
    )


@router.get("")
# Documentação: Lista list_workers, segundo o contrato e as verificações deste módulo.
def list_workers(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return [worker_data(row) for row in WorkerService(session, user.id).workers()]


@router.get("/{identifier}")
# Documentação: Implementa status como parte do fluxo descrito para este arquivo.
def status(
    identifier: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return invoke(session, user.id, lambda service: worker_data(service.worker(identifier)))


@router.post("/{identifier}/commands", status_code=202)
# Documentação: Implementa command como parte do fluxo descrito para este arquivo.
def command(
    identifier: UUID,
    data: CommandRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    args = data.model_dump(mode="json", exclude={"request_id", "kind"}, exclude_none=True)
    return invoke(
        session,
        user.id,
        lambda service: command_data(service.queue(data.kind, args, data.request_id, identifier)),
    )


@router.get("/{identifier}/commands")
# Documentação: Implementa commands como parte do fluxo descrito para este arquivo.
def commands(
    identifier: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return invoke(
        session,
        user.id,
        lambda service: [command_data(row) for row in service.commands(identifier)],
    )


@router.get("/{identifier}/snapshots")
# Documentação: Implementa snapshots como parte do fluxo descrito para este arquivo.
def snapshots(
    identifier: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return invoke(
        session,
        user.id,
        lambda service: [snapshot_data(row) for row in service.snapshots(identifier)],
    )
