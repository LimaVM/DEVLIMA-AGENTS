from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.errors import AgentError
from app.agent.memory_manager import MemoryManager
from app.db.session import get_session
from app.models import AuditLog, Memory, MemoryCandidate, User
from app.schemas.memories import CandidateResponse, MemoryCreate, MemoryResponse
from app.security import get_current_user

router = APIRouter(prefix="/memories", tags=["memories"])


@router.get("", response_model=list[MemoryResponse])
# Documentação: Lista list_memories, segundo o contrato e as verificações deste módulo.
def list_memories(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.scalars(
        select(Memory)
        .where(Memory.user_id == user.id, Memory.is_active.is_(True))
        .order_by(Memory.updated_at.desc(), Memory.id)
        .offset(offset)
        .limit(limit)
    ).all()


@router.post("", response_model=MemoryResponse, status_code=201)
# Documentação: Cria create_memory, segundo o contrato e as verificações deste módulo.
def create_memory(
    data: MemoryCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    row = MemoryManager(session, user.id).create(data.content, data.category)
    session.commit()
    return row


@router.delete("/{identifier}", status_code=204)
# Documentação: Implementa deactivate_memory como parte do fluxo descrito para este arquivo.
def deactivate_memory(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    row = session.scalar(
        select(Memory).where(Memory.id == identifier, Memory.user_id == user.id).with_for_update()
    )
    if row is None:
        raise HTTPException(404, "not_found")
    row.is_active, row.updated_at = False, datetime.now(UTC)
    session.add(
        AuditLog(user_id=user.id, event="memory.deactivated", details={"memory_id": str(row.id)})
    )
    session.commit()
    return Response(status_code=204)


@router.get("/candidates", response_model=list[CandidateResponse])
# Documentação: Lista list_candidates, segundo o contrato e as verificações deste módulo.
def list_candidates(
    status: str = Query("PENDING", pattern="^(PENDING|ACCEPTED|REJECTED)$"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.scalars(
        select(MemoryCandidate)
        .where(MemoryCandidate.user_id == user.id, MemoryCandidate.status == status)
        .order_by(MemoryCandidate.created_at.desc(), MemoryCandidate.id)
        .offset(offset)
        .limit(limit)
    ).all()


@router.post("/candidates/{identifier}/accept", response_model=MemoryResponse)
# Documentação: Implementa accept_candidate como parte do fluxo descrito para este arquivo.
def accept_candidate(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    try:
        row = MemoryManager(session, user.id).accept(identifier)
        session.commit()
        return row
    except AgentError as error:
        raise HTTPException(error.status_code, error.code) from None


@router.post("/candidates/{identifier}/reject", status_code=204)
# Documentação: Implementa reject_candidate como parte do fluxo descrito para este arquivo.
def reject_candidate(
    identifier: UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    row = session.scalar(
        select(MemoryCandidate)
        .where(MemoryCandidate.id == identifier, MemoryCandidate.user_id == user.id)
        .with_for_update()
    )
    if row is None:
        raise HTTPException(404, "not_found")
    if row.status == "ACCEPTED":
        raise HTTPException(409, "candidate_already_accepted")
    row.status, row.rejection_reason = "REJECTED", "user_rejected"
    session.add(
        AuditLog(
            user_id=user.id,
            event="memory.candidate_rejected",
            details={"candidate_id": str(row.id)},
        )
    )
    session.commit()
    return Response(status_code=204)
