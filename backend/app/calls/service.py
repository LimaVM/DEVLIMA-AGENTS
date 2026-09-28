from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import select

from app.agent.errors import AgentError
from app.models import AuditLog, Conversation, Device, OutboxEvent, User
from app.models.calls import CallSession


def state(row):
    return {
        "id": str(row.id),
        "device_id": str(row.device_id),
        "incoming_event_id": str(row.incoming_event_id),
        "conversation_id": str(row.conversation_id),
        "reason": row.reason,
        "status": row.status,
        "started_at": row.started_at.isoformat(),
        "ended_at": row.ended_at.isoformat() if row.ended_at else None,
    }


def publish(session, owner, event, payload, key):
    session.add(OutboxEvent(user_id=owner, type=event, payload=payload, dedupe_key=key))


def audit(session, owner, event, identifier):
    session.add(AuditLog(user_id=owner, event=event, details={"id": str(identifier)}))


class CallService:
    def __init__(self, session, owner, device_id=None):
        self.session, self.owner, self.device_id = session, owner, device_id

    def device(self):
        row = self.session.get(Device, self.device_id)
        if row is None or row.user_id != self.owner or row.revoked:
            raise AgentError("device_unavailable", 403)

    def incoming(self, identifier):
        row = self.session.scalar(
            select(OutboxEvent)
            .where(
                OutboxEvent.id == identifier,
                OutboxEvent.user_id == self.owner,
                OutboxEvent.type == "call.incoming",
            )
            .with_for_update()
        )
        if row is None:
            raise AgentError("call_not_found", 404)
        return row

    def answer(self, identifier):
        self.device()
        # Serializes different incoming calls and devices for this account.
        self.session.scalar(select(User).where(User.id == self.owner).with_for_update())
        self.expire()
        event = self.incoming(identifier)
        previous = self.session.scalar(
            select(CallSession).where(CallSession.incoming_event_id == identifier)
        )
        if previous:
            if previous.device_id != self.device_id:
                raise AgentError("call_answered_on_another_device")
            return state(previous)
        if event.status != "PENDING" or event.created_at < datetime.now(UTC) - timedelta(
            seconds=120
        ):
            raise AgentError("call_no_longer_ringing")
        active = self.session.scalar(
            select(CallSession).where(
                CallSession.user_id == self.owner, CallSession.status == "ACTIVE"
            )
        )
        if active:
            raise AgentError("call_already_active")
        conversation = Conversation(
            user_id=self.owner, title="Chamada: " + event.payload.get("text", "Agente")[:80]
        )
        self.session.add(conversation)
        self.session.flush()
        row = CallSession(
            id=uuid4(),
            user_id=self.owner,
            device_id=self.device_id,
            incoming_event_id=event.id,
            conversation_id=conversation.id,
            reason=event.payload.get("text", "Conversar com o agente"),
            status="ACTIVE",
        )
        self.session.add(row)
        self.session.flush()
        event.status = "CANCELLED"
        event.payload = {**event.payload, "resolution": "ANSWERED"}
        result = state(row)
        publish(
            self.session,
            self.owner,
            "call.state",
            {"session": result, "event_id": str(event.id)},
            f"call:{row.id}:answered",
        )
        audit(self.session, self.owner, "call.answered", row.id)
        return result

    def reject(self, identifier):
        self.device()
        event = self.incoming(identifier)
        if event.payload.get("resolution") == "REJECTED":
            return {"event_id": str(identifier), "status": "REJECTED"}
        if event.status != "PENDING":
            raise AgentError("call_no_longer_ringing")
        event.status = "CANCELLED"
        event.payload = {**event.payload, "resolution": "REJECTED"}
        publish(
            self.session,
            self.owner,
            "call.dismissed",
            {"event_id": str(event.id), "status": "REJECTED"},
            f"call:{event.id}:rejected",
        )
        audit(self.session, self.owner, "call.rejected", event.id)
        return {"event_id": str(identifier), "status": "REJECTED"}

    def owned(self, identifier, device=False):
        row = self.session.scalar(
            select(CallSession)
            .where(CallSession.id == identifier, CallSession.user_id == self.owner)
            .with_for_update()
        )
        if row is None:
            raise AgentError("call_not_found", 404)
        if device and row.device_id != self.device_id:
            raise AgentError("call_device_mismatch", 403)
        return row

    def finish(self, row, status):
        row.status, row.ended_at = status, datetime.now(UTC)
        publish(
            self.session,
            self.owner,
            "call.state",
            {"session": state(row), "event_id": str(row.incoming_event_id)},
            f"call:{row.id}:ended",
        )
        audit(self.session, self.owner, "call.ended", row.id)

    def end(self, identifier):
        self.device()
        row = self.owned(identifier, True)
        if row.status == "ACTIVE":
            self.finish(row, "ENDED")
        return state(row)

    def touch(self, identifier):
        self.device()
        row = self.owned(identifier, True)
        if row.status != "ACTIVE" or self.expired(row, datetime.now(UTC)):
            raise AgentError("call_not_active")
        row.last_active_at = datetime.now(UTC)
        return row.conversation_id

    @staticmethod
    def expired(row, now):
        return row.last_active_at < now - timedelta(minutes=10) or row.started_at < now - timedelta(
            minutes=30
        )

    def expire(self, now=None):
        now = now or datetime.now(UTC)
        for event in self.session.scalars(
            select(OutboxEvent)
            .where(
                OutboxEvent.user_id == self.owner,
                OutboxEvent.type == "call.incoming",
                OutboxEvent.status == "PENDING",
                OutboxEvent.created_at < now - timedelta(seconds=120),
            )
            .with_for_update(skip_locked=True)
        ):
            event.status = "CANCELLED"
            event.payload = {**event.payload, "resolution": "MISSED"}
            publish(
                self.session,
                self.owner,
                "call.dismissed",
                {"event_id": str(event.id), "status": "MISSED"},
                f"call:{event.id}:missed",
            )
            audit(self.session, self.owner, "call.missed", event.id)
        for row in self.session.scalars(
            select(CallSession)
            .where(CallSession.user_id == self.owner, CallSession.status == "ACTIVE")
            .with_for_update(skip_locked=True)
        ):
            if self.expired(row, now):
                self.finish(row, "EXPIRED")
