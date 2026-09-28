from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.agent.errors import AgentError
from app.models import AuditLog, User
from app.models.planning import OutboxEvent, Schedule, Task
from app.planning.recurrence import first_occurrence


def aware(value):
    if value is None or isinstance(value, datetime):
        return value.astimezone(UTC) if value else None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def task_data(row: Task):
    return {
        "id": str(row.id),
        "title": row.title,
        "description": row.description,
        "status": row.status,
        "due_at": row.due_at.isoformat() if row.due_at else None,
    }


def schedule_data(row: Schedule):
    return {
        "id": str(row.id),
        "kind": row.kind,
        "text": row.text,
        "timezone": row.timezone,
        "start_at": row.start_at.isoformat(),
        "next_run_at": row.next_run_at.isoformat() if row.next_run_at else None,
        "rrule": row.rrule,
        "status": row.status,
        "version": row.version,
    }


class PlanningService:
    def __init__(self, session: Session, user_id: UUID):
        self.session = session
        self.user_id = user_id
        self.user = session.get(User, user_id)
        if self.user is None:
            raise AgentError("not_found", 404)

    def audit(self, event, identifier):
        self.session.add(
            AuditLog(user_id=self.user_id, event=event, details={"id": str(identifier)})
        )

    def event(self, type, payload, schedule_id=None, dedupe=None):
        identifier = uuid4()
        row = OutboxEvent(
            id=identifier,
            user_id=self.user_id,
            type=type,
            payload=payload,
            schedule_id=schedule_id,
            dedupe_key=dedupe or str(identifier),
            status="PENDING",
        )
        self.session.add(row)
        return row

    def task(self, identifier):
        row = self.session.scalar(
            select(Task)
            .where(Task.id == identifier, Task.user_id == self.user_id)
            .with_for_update()
        )
        if row is None:
            raise AgentError("not_found", 404)
        return row

    def create_task(self, data):
        title = data["title"].strip()
        if not title:
            raise AgentError("empty_title", 422)
        row = Task(
            user_id=self.user_id,
            title=title,
            description=data.get("description"),
            due_at=aware(data.get("due_at")),
            status="OPEN",
        )
        self.session.add(row)
        self.session.flush()
        self.audit("task.created", row.id)
        self.event("task.updated", task_data(row))
        return row

    def update_task(self, identifier, data):
        row = self.task(identifier)
        if not data:
            raise AgentError("empty_update", 422)
        if "title" in data:
            if not data["title"] or not data["title"].strip():
                raise AgentError("empty_title", 422)
            row.title = data["title"].strip()
        if "description" in data:
            row.description = data["description"]
        if "due_at" in data:
            row.due_at = aware(data["due_at"])
        row.updated_at = datetime.now(UTC)
        self.audit("task.updated", row.id)
        self.event("task.updated", task_data(row))
        return row

    def complete_task(self, identifier):
        row = self.task(identifier)
        if row.status != "COMPLETED":
            row.status = "COMPLETED"
            row.updated_at = datetime.now(UTC)
            self.audit("task.completed", row.id)
            self.event("task.updated", task_data(row))
        return row

    def date_query(self, query, column, day):
        if day:
            try:
                selected = date.fromisoformat(str(day))
            except ValueError:
                raise AgentError("invalid_date", 422) from None
            start = datetime.combine(selected, time(), ZoneInfo(self.user.timezone))
            query = query.where(
                column >= start.astimezone(UTC),
                column < (start + timedelta(days=1)).astimezone(UTC),
            )
        return query

    def list_tasks(self, day=None, status=None, limit=100, offset=0):
        query = select(Task).where(Task.user_id == self.user_id)
        if status:
            query = query.where(Task.status == status)
        query = self.date_query(query, Task.due_at, day)
        return self.session.scalars(
            query.order_by(Task.created_at.desc(), Task.id).offset(offset).limit(limit)
        ).all()

    def schedule(self, identifier, kind):
        row = self.session.scalar(
            select(Schedule)
            .where(
                Schedule.id == identifier, Schedule.user_id == self.user_id, Schedule.kind == kind
            )
            .with_for_update()
        )
        if row is None:
            raise AgentError("not_found", 404)
        return row

    def create_schedule(self, kind, data):
        now = datetime.now(UTC)
        start = aware(data["datetime"])
        if start <= now or start > now + timedelta(days=366):
            raise AgentError("schedule_date_out_of_range", 422)
        text = (
            data.get("text") if kind == "REMINDER" else data.get("reason", "Conversar com o agente")
        )
        if not text or not text.strip():
            raise AgentError("empty_text", 422)
        next_run = first_occurrence(data.get("rrule"), start, self.user.timezone)
        if next_run > now + timedelta(days=366):
            raise AgentError("schedule_date_out_of_range", 422)
        row = Schedule(
            user_id=self.user_id,
            kind=kind,
            text=text.strip(),
            timezone=self.user.timezone,
            start_at=start,
            next_run_at=next_run,
            rrule=data.get("rrule"),
            status="SCHEDULED",
            version=1,
        )
        self.session.add(row)
        self.session.flush()
        self.audit("schedule.created", row.id)
        return row

    def update_schedule(self, identifier, data):
        row = self.schedule(identifier, "REMINDER")
        if row.status != "SCHEDULED":
            raise AgentError("schedule_not_active")
        if not data:
            raise AgentError("empty_update", 422)
        if "text" in data:
            if not data["text"] or not data["text"].strip():
                raise AgentError("empty_text", 422)
            row.text = data["text"].strip()
        if "datetime" in data:
            start = aware(data["datetime"])
            now = datetime.now(UTC)
            if not start or not now < start <= now + timedelta(days=366):
                raise AgentError("schedule_date_out_of_range", 422)
            row.start_at = start
        if "rrule" in data:
            row.rrule = data["rrule"]
        row.next_run_at = (
            first_occurrence(row.rrule, row.start_at, row.timezone)
            if "datetime" in data or "rrule" in data
            else row.next_run_at
        )
        if row.next_run_at <= datetime.now(UTC):
            raise AgentError("schedule_date_out_of_range", 422)
        row.version += 1
        row.updated_at = datetime.now(UTC)
        self.session.execute(
            update(OutboxEvent)
            .where(OutboxEvent.schedule_id == row.id, OutboxEvent.status == "PENDING")
            .values(status="CANCELLED")
        )
        self.audit("schedule.updated", row.id)
        return row

    def cancel_schedule(self, identifier, kind):
        row = self.schedule(identifier, kind)
        if row.status != "CANCELLED":
            row.status, row.next_run_at = "CANCELLED", None
            row.version += 1
            row.updated_at = datetime.now(UTC)
            self.session.execute(
                update(OutboxEvent)
                .where(OutboxEvent.schedule_id == row.id, OutboxEvent.status == "PENDING")
                .values(status="CANCELLED")
            )
            self.audit("schedule.cancelled", row.id)
            if kind == "CALL":
                self.event(
                    "call.cancelled",
                    {"schedule_id": str(row.id)},
                    schedule_id=row.id,
                    dedupe=f"cancel:{row.id}:{row.version}",
                )
        return row

    def list_schedules(self, kind, day=None, status=None, limit=100, offset=0):
        query = select(Schedule).where(Schedule.user_id == self.user_id, Schedule.kind == kind)
        if status:
            query = query.where(Schedule.status == status)
        query = self.date_query(query, Schedule.next_run_at, day)
        return self.session.scalars(
            query.order_by(Schedule.next_run_at.asc().nulls_last(), Schedule.id)
            .offset(offset)
            .limit(limit)
        ).all()
