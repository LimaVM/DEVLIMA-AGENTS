import argparse
import logging
import signal
from datetime import UTC, datetime, timedelta
from threading import Event
from uuid import UUID, uuid5

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.models import AuditLog, User
from app.models.planning import OutboxEvent, Schedule, ScheduledEvent, SchedulerHeartbeat
from app.planning.recurrence import next_occurrence

NAMESPACE = UUID("13d7b843-49eb-47bb-b9bd-bb842df8988a")
logger = logging.getLogger("devlima.scheduler")


# Documentação: Implementa tick como parte do fluxo descrito para este arquivo.
def tick(session: Session, now: datetime | None = None, batch_size: int = 100) -> int:
    now = now or datetime.now(UTC)
    rows = session.scalars(
        select(Schedule)
        .join(User, User.id == Schedule.user_id)
        .where(
            Schedule.status == "SCHEDULED", Schedule.next_run_at <= now, User.is_active.is_(True)
        )
        .order_by(Schedule.next_run_at, Schedule.id)
        .limit(batch_size)
        .with_for_update(skip_locked=True, of=Schedule)
    ).all()
    for row in rows:
        scheduled = row.next_run_at
        key = f"schedule:{row.id}:{row.version}:{scheduled.isoformat()}"
        event_id = uuid5(NAMESPACE, key)
        session.execute(
            insert(ScheduledEvent)
            .values(
                id=event_id,
                user_id=row.user_id,
                schedule_id=row.id,
                version=row.version,
                scheduled_at=scheduled,
                executed_at=now,
                status="EMITTED",
            )
            .on_conflict_do_nothing(
                index_elements=[
                    ScheduledEvent.schedule_id,
                    ScheduledEvent.version,
                    ScheduledEvent.scheduled_at,
                ]
            )
        )
        session.execute(
            insert(OutboxEvent)
            .values(
                id=event_id,
                user_id=row.user_id,
                schedule_id=row.id,
                type="reminder.triggered" if row.kind == "REMINDER" else "call.incoming",
                status="PENDING",
                dedupe_key=key,
                payload={
                    "schedule_id": str(row.id),
                    "text": row.text,
                    "scheduled_at": scheduled.isoformat(),
                    "timezone": row.timezone,
                    "late": (now - scheduled).total_seconds() > 30,
                    "recurring": bool(row.rrule),
                },
                created_at=now,
            )
            .on_conflict_do_nothing(index_elements=[OutboxEvent.dedupe_key])
        )
        row.next_run_at = next_occurrence(row.rrule, row.start_at, row.timezone, now)
        row.status = "SCHEDULED" if row.next_run_at else "COMPLETED"
        row.updated_at = now
        session.add(
            AuditLog(
                user_id=row.user_id,
                event="schedule.emitted",
                details={
                    "schedule_id": str(row.id),
                    "event_id": str(event_id),
                    "version": row.version,
                },
            )
        )
    session.execute(
        insert(SchedulerHeartbeat)
        .values(name="scheduler", last_tick_at=now, processed=len(rows))
        .on_conflict_do_update(
            index_elements=[SchedulerHeartbeat.name],
            set_={"last_tick_at": now, "processed": len(rows)},
        )
    )
    session.commit()
    return len(rows)


# Documentação: Coordena a entrada de linha de comando deste arquivo: Busca agendamentos vencidos
# com locks PostgreSQL, cria ocorrência/outbox em transação, avança recorrência e publica
# heartbeat para readiness operacional.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["run", "once", "health"])
    args = parser.parse_args()
    if args.command == "health":
        with Session(get_engine()) as session:
            row = session.get(SchedulerHeartbeat, "scheduler")
            if row is None or datetime.now(UTC) - row.last_tick_at > timedelta(
                seconds=max(30, get_settings().scheduler_poll_seconds * 3)
            ):
                raise SystemExit(1)
        return

    # Documentação: Processa agendamentos vencidos e conserva ocorrência/evento/avanço de
    # recorrência em transação.
    def run_tick():
        try:
            with Session(get_engine(), expire_on_commit=False) as session:
                return tick(session)
        except Exception:
            # Neither SQL parameters nor event payloads belong in daemon logs.
            logger.error("Scheduler tick failed; retry on next interval")
            if args.command == "once":
                raise

    if args.command == "once":
        print(run_tick())
        return
    stop = Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    scheduler = BackgroundScheduler(timezone=UTC)
    scheduler.add_job(
        run_tick,
        "interval",
        seconds=get_settings().scheduler_poll_seconds,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=30,
    )
    run_tick()
    scheduler.start()
    stop.wait()
    scheduler.shutdown(wait=True)


if __name__ == "__main__":
    main()
