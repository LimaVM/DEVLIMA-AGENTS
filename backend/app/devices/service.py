import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from sqlalchemy import or_, select, text
from sqlalchemy.dialects.postgresql import insert

from app.agent.errors import AgentError
from app.models import AuditLog, OutboxEvent, User
from app.models.devices import Device, EventDelivery, RefreshFamily, RefreshToken


def token_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


def register(session, identifier, owner, name="Android"):
    identifier = UUID(str(identifier))
    session.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
        {"key": f"device:{identifier}"},
    )
    device = session.get(Device, identifier)
    if device is not None:
        if device.user_id != owner or device.revoked:
            raise AgentError("device_unavailable", 403)
        device.last_seen_at = datetime.now(UTC)
    else:
        device = Device(id=identifier, user_id=owner, name=name)
        session.add(device)
    session.flush()
    return device


def issue_session(session, user, device_id, settings):
    from app.security import create_token

    device = register(session, device_id, user.id)
    # A login creates one new family and invalidates previous sessions of this device.
    for previous in session.scalars(
        select(RefreshFamily)
        .where(RefreshFamily.device_id == device.id, RefreshFamily.revoked.is_(False))
        .with_for_update()
    ):
        previous.revoked = True
    family = RefreshFamily(
        user_id=user.id,
        device_id=device.id,
        token_version=user.token_version,
        expires_at=datetime.now(UTC) + timedelta(days=30),
    )
    session.add(family)
    session.flush()
    opaque = secrets.token_urlsafe(48)
    session.add(RefreshToken(token_hash=token_hash(opaque), family_id=family.id))
    return {
        "access_token": create_token(user, settings, family.id),
        "refresh_token": opaque,
        "expires_in": settings.jwt_ttl_minutes * 60,
        "token_type": "bearer",
    }


def rotate_session(session, opaque, settings):
    from app.security import create_token

    digest = token_hash(opaque)
    record = session.get(RefreshToken, digest)
    if record is None:
        raise AgentError("invalid_refresh", 401)
    family = session.scalar(
        select(RefreshFamily).where(RefreshFamily.id == record.family_id).with_for_update()
    )
    # Serialize against refresh and re-read token usage after acquiring family lock.
    session.refresh(record)
    user, device = session.get(User, family.user_id), session.get(Device, family.device_id)
    invalid = (
        family.revoked
        or family.expires_at <= datetime.now(UTC)
        or user is None
        or not user.is_active
        or family.token_version != user.token_version
        or device is None
        or device.revoked
    )
    if record.used or invalid:
        family.revoked = True
        session.add(
            AuditLog(
                user_id=family.user_id,
                event="auth.refresh_rejected",
                details={"family_id": str(family.id), "reuse": record.used},
            )
        )
        session.commit()
        raise AgentError("invalid_refresh", 401)
    record.used = True
    new = secrets.token_urlsafe(48)
    session.add(RefreshToken(token_hash=token_hash(new), family_id=family.id))
    session.add(
        AuditLog(user_id=user.id, event="auth.refreshed", details={"family_id": str(family.id)})
    )
    session.flush()
    return {
        "access_token": create_token(user, settings, family.id),
        "refresh_token": new,
        "expires_in": settings.jwt_ttl_minutes * 60,
        "token_type": "bearer",
    }


def authorize_claims(session, claims):
    user = session.get(User, UUID(claims["sub"]))
    if user is None or not user.is_active or user.token_version != claims["ver"]:
        raise jwt.InvalidTokenError("revoked")
    if "sid" in claims:
        family = session.get(RefreshFamily, UUID(claims["sid"]))
        if (
            family is None
            or family.user_id != user.id
            or family.revoked
            or family.expires_at <= datetime.now(UTC)
        ):
            raise jwt.InvalidTokenError("revoked_session")
        device = session.get(Device, family.device_id)
        if device is None or device.revoked:
            raise jwt.InvalidTokenError("revoked_device")
    return user


def logout(session, claims):
    if "sid" in claims:
        family = session.get(RefreshFamily, UUID(claims["sid"]))
        if family and family.user_id == UUID(claims["sub"]):
            family.revoked = True
    session.commit()


def pending(session, owner, device_id, now=None):
    now = now or datetime.now(UTC)
    device = session.get(Device, device_id)
    if device is None or device.user_id != owner or device.revoked:
        raise AgentError("device_unavailable", 403)
    device.last_seen_at = now
    query = (
        select(OutboxEvent)
        .outerjoin(
            EventDelivery,
            (EventDelivery.event_id == OutboxEvent.id) & (EventDelivery.device_id == device_id),
        )
        .where(
            OutboxEvent.user_id == owner,
            OutboxEvent.status == "PENDING",
            EventDelivery.acknowledged_at.is_(None),
            or_(
                EventDelivery.sent_at.is_(None),
                EventDelivery.sent_at <= now - timedelta(seconds=15),
            ),
        )
        .order_by(OutboxEvent.created_at, OutboxEvent.id)
        .limit(50)
    )
    events = session.scalars(query).all()
    for event in events:
        session.execute(
            insert(EventDelivery)
            .values(device_id=device_id, event_id=event.id, user_id=owner, sent_at=now, attempts=1)
            .on_conflict_do_update(
                index_elements=[EventDelivery.device_id, EventDelivery.event_id],
                set_={"sent_at": now, "attempts": EventDelivery.attempts + 1},
            )
        )
    session.commit()
    return [
        {
            "event_id": str(event.id),
            "timestamp": event.created_at.isoformat(),
            "type": event.type,
            "payload": event.payload,
        }
        for event in events
    ]


def acknowledge(session, owner, device_id, event_id):
    device = session.get(Device, device_id)
    row = session.get(EventDelivery, (device_id, event_id))
    if (
        device is None
        or device.user_id != owner
        or device.revoked
        or row is None
        or row.user_id != owner
    ):
        raise AgentError("event_not_found", 404)
    if row.acknowledged_at is None:
        row.acknowledged_at = datetime.now(UTC)
    session.commit()
