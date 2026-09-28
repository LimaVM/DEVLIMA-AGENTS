from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models import AuditLog, User
from app.models.devices import Device, RefreshFamily
from app.security import get_current_user

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("")
# Documentação: Implementa devices como parte do fluxo descrito para este arquivo.
def devices(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return [
        {"id": row.id, "name": row.name, "revoked": row.revoked, "last_seen_at": row.last_seen_at}
        for row in session.scalars(
            select(Device)
            .where(Device.user_id == user.id)
            .order_by(Device.created_at.desc())
            .limit(100)
        )
    ]


@router.post("/{identifier}/revoke", status_code=204)
# Documentação: Revoga revoke, segundo o contrato e as verificações deste módulo.
def revoke(
    identifier: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    row = session.scalar(
        select(Device).where(Device.id == identifier, Device.user_id == user.id).with_for_update()
    )
    if row is None:
        raise HTTPException(404, "not_found")
    row.revoked = True
    for family in session.scalars(
        select(RefreshFamily).where(RefreshFamily.device_id == row.id).with_for_update()
    ):
        family.revoked = True
    session.add(
        AuditLog(user_id=user.id, event="device.revoked", details={"device_id": str(row.id)})
    )
    session.commit()
    return Response(status_code=204)
