from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from test_context import history

from app.agent.action_engine import ActionEngine
from app.agent.action_parser import ActionProposal
from app.agent.errors import AgentError
from app.config import get_settings
from app.db.session import get_engine
from app.models import OutboxEvent, Schedule, ScheduledEvent, SchedulerHeartbeat, Task, User
from app.planning.recurrence import first_occurrence, next_occurrence
from app.planning.scheduler import tick
from app.planning.service import PlanningService
from app.security import create_token


# Documentação: Implementa headers como parte do fluxo descrito para este arquivo.
def headers(user):
    return {"Authorization": f"Bearer {create_token(user, get_settings())}"}


# Documentação: Implementa future como parte do fluxo descrito para este arquivo.
def future(seconds=60):
    return datetime.now(UTC) + timedelta(seconds=seconds)


# Documentação: Verifica o cenário test_task_api_lifecycle_timezone_and_tenant; as condições e
# resultados esperados aparecem nos asserts.
def test_task_api_lifecycle_timezone_and_tenant(client, session, user):
    auth = headers(user)
    response = client.post(
        "/tasks", headers=auth, json={"title": "Pagar conta", "due_at": "2026-10-01T23:30:00-03:00"}
    )
    assert response.status_code == 201
    identifier = response.json()["id"]
    assert response.json()["due_at"] == "2026-10-02T02:30:00Z"
    assert len(client.get("/tasks?date=2026-10-01", headers=auth).json()) == 1
    assert client.get("/tasks?date=2026-10-02", headers=auth).json() == []
    other = User(username="other", password_hash=user.password_hash, timezone=user.timezone)
    session.add(other)
    session.commit()
    assert (
        client.patch(
            f"/tasks/{identifier}", headers=headers(other), json={"title": "Ataque"}
        ).status_code
        == 404
    )
    assert (
        client.patch(
            f"/tasks/{identifier}", headers=auth, json={"description": "Detalhes", "due_at": None}
        ).status_code
        == 200
    )
    assert (
        client.post(f"/tasks/{identifier}/complete", headers=auth).json()["status"] == "COMPLETED"
    )
    before = session.scalar(select(func.count()).select_from(OutboxEvent))
    assert client.post(f"/tasks/{identifier}/complete", headers=auth).status_code == 200
    assert session.scalar(select(func.count()).select_from(OutboxEvent)) == before
    assert client.get("/tasks?status=OPEN", headers=auth).json() == []
    assert client.get("/tasks").status_code == 401


@pytest.mark.parametrize(
    "payload",
    [
        {"title": " "},
        {"title": "x", "due_at": "2026-10-01T12:00:00"},
        {"title": "x", "command": "ls"},
    ],
)
# Documentação: Verifica o cenário test_task_invalid_input; as condições e resultados esperados
# aparecem nos asserts.
def test_task_invalid_input(client, user, payload):
    assert client.post("/tasks", headers=headers(user), json=payload).status_code == 422


# Documentação: Verifica o cenário test_reminder_api_create_update_cancel_and_call; as condições e
# resultados esperados aparecem nos asserts.
def test_reminder_api_create_update_cancel_and_call(client, session, user):
    auth = headers(user)
    created = client.post(
        "/reminders", headers=auth, json={"text": "Café", "datetime": future().isoformat()}
    )
    assert created.status_code == 201
    identifier = created.json()["id"]
    updated = client.patch(
        f"/reminders/{identifier}",
        headers=auth,
        json={"text": "Água", "datetime": future(120).isoformat()},
    )
    assert updated.status_code == 200 and updated.json()["version"] == 2
    assert client.delete(f"/reminders/{identifier}", headers=auth).json()["status"] == "CANCELLED"
    assert (
        client.patch(f"/reminders/{identifier}", headers=auth, json={"text": "x"}).status_code
        == 409
    )
    call = client.post(
        "/scheduled-calls",
        headers=auth,
        json={"datetime": future().isoformat(), "reason": "Revisar o dia"},
    )
    assert call.status_code == 201
    assert client.delete(f"/scheduled-calls/{call.json()['id']}", headers=auth).status_code == 200
    assert session.scalar(select(OutboxEvent).where(OutboxEvent.type == "call.cancelled"))
    assert client.get("/scheduled-calls", headers=auth).json()[0]["status"] == "CANCELLED"
    assert client.get("/reminders?status=SCHEDULED", headers=auth).json() == []


@pytest.mark.parametrize("delta", [-10, 367 * 86400])
# Documentação: Verifica o cenário test_past_or_distant_schedule_rejected; as condições e
# resultados esperados aparecem nos asserts.
def test_past_or_distant_schedule_rejected(client, user, delta):
    response = client.post(
        "/reminders",
        headers=headers(user),
        json={"text": "x", "datetime": future(delta).isoformat()},
    )
    assert response.status_code == 422 and response.json()["detail"] == "schedule_date_out_of_range"


@pytest.mark.parametrize(
    "rrule",
    [
        "FREQ=SECONDLY",
        "FREQ=DAILY;COUNT=0",
        "FREQ=DAILY;COUNT=2;UNTIL=20261001T000000Z",
        "DTSTART:20260101\nRRULE:FREQ=DAILY",
        "FREQ=DAILY;FREQ=WEEKLY",
        "FREQ=DAILY;BYSECOND=1",
        "FREQ=DAILY;INTERVAL=0",
    ],
)
# Documentação: Verifica o cenário test_recurrence_rejected; as condições e resultados esperados
# aparecem nos asserts.
def test_recurrence_rejected(rrule):
    with pytest.raises(AgentError):
        first_occurrence(rrule, future(), "America/Sao_Paulo")


# Documentação: Verifica o cenário test_weekly_recurrence_timezone_and_count; as condições e
# resultados esperados aparecem nos asserts.
def test_weekly_recurrence_timezone_and_count():
    start = datetime(2026, 9, 28, 23, tzinfo=UTC)
    first = first_occurrence("FREQ=WEEKLY;BYDAY=SU;COUNT=2", start, "America/Sao_Paulo")
    assert first == datetime(2026, 10, 4, 23, tzinfo=UTC)
    second = next_occurrence("FREQ=WEEKLY;BYDAY=SU;COUNT=2", start, "America/Sao_Paulo", first)
    assert second == first + timedelta(days=7)
    assert (
        next_occurrence("FREQ=WEEKLY;BYDAY=SU;COUNT=2", start, "America/Sao_Paulo", second) is None
    )


# Documentação: Verifica o cenário test_recurrence_preserves_wall_clock_across_dst; as condições e
# resultados esperados aparecem nos asserts.
def test_recurrence_preserves_wall_clock_across_dst():
    start = datetime(2026, 10, 31, 13, tzinfo=UTC)
    next_run = next_occurrence("FREQ=DAILY", start, "America/New_York", start)
    assert next_run == datetime(2026, 11, 1, 14, tzinfo=UTC)


# Documentação: Verifica o cenário test_scheduler_emits_once_across_sessions; as condições e
# resultados esperados aparecem nos asserts.
def test_scheduler_emits_once_across_sessions(session, user):
    service = PlanningService(session, user.id)
    row = service.create_schedule("REMINDER", {"text": "Café", "datetime": future()})
    due = row.next_run_at
    session.commit()
    assert tick(session, due + timedelta(seconds=1)) == 1
    assert tick(session, due + timedelta(seconds=2)) == 0
    with Session(get_engine()) as fresh:
        assert fresh.scalar(select(func.count()).select_from(ScheduledEvent)) == 1
        event = fresh.scalar(select(OutboxEvent))
        assert event.type == "reminder.triggered" and event.payload["text"] == "Café"
        assert fresh.get(Schedule, row.id).status == "COMPLETED"
        assert fresh.get(SchedulerHeartbeat, "scheduler")


# Documentação: Verifica o cenário test_scheduler_coalesces_missed_recurrences; as condições e
# resultados esperados aparecem nos asserts.
def test_scheduler_coalesces_missed_recurrences(session, user):
    row = PlanningService(session, user.id).create_schedule(
        "REMINDER", {"text": "Revisão", "datetime": future(), "rrule": "FREQ=DAILY;COUNT=10"}
    )
    due = row.next_run_at
    session.commit()
    now = due + timedelta(days=4, hours=1)
    assert tick(session, now) == 1
    assert row.next_run_at == due + timedelta(days=5)
    assert session.scalar(select(OutboxEvent)).payload["late"]
    assert tick(session, now) == 0


# Documentação: Verifica o cenário test_scheduler_concurrent_claims; as condições e resultados
# esperados aparecem nos asserts.
def test_scheduler_concurrent_claims(session, user):
    service = PlanningService(session, user.id)
    now = future(120)
    for i in range(20):
        service.create_schedule("CALL", {"reason": str(i), "datetime": now})
    session.commit()

    # Documentação: Implementa test_scheduler_concurrent_claims.execute como parte do fluxo
    # descrito para este arquivo.
    def execute(_):
        with Session(get_engine(), expire_on_commit=False) as fresh:
            return tick(fresh, now + timedelta(seconds=1))

    with ThreadPoolExecutor(max_workers=4) as pool:
        counts = list(pool.map(execute, range(4)))
    assert sum(counts) == 20
    assert session.scalar(select(func.count()).select_from(ScheduledEvent)) == 20
    assert session.scalar(select(func.count()).select_from(OutboxEvent)) == 20


# Documentação: Verifica o cenário test_crash_before_commit_leaves_event_due; as condições e
# resultados esperados aparecem nos asserts.
def test_crash_before_commit_leaves_event_due(session, user, monkeypatch):
    row = PlanningService(session, user.id).create_schedule("CALL", {"datetime": future()})
    identifier, due = row.id, row.next_run_at
    session.commit()

    # Documentação: Implementa test_crash_before_commit_leaves_event_due.fail_commit como parte do
    # fluxo descrito para este arquivo.
    def fail_commit():
        raise RuntimeError("simulated crash")

    with monkeypatch.context() as patch:
        patch.setattr(session, "commit", fail_commit)
        with pytest.raises(RuntimeError):
            tick(session, due)
        session.rollback()
    assert session.get(Schedule, identifier).status == "SCHEDULED"
    assert session.scalar(select(func.count()).select_from(OutboxEvent)) == 0
    assert tick(session, due) == 1


# Documentação: Verifica o cenário test_cancel_and_inactive_user_do_not_trigger; as condições e
# resultados esperados aparecem nos asserts.
def test_cancel_and_inactive_user_do_not_trigger(session, user):
    service = PlanningService(session, user.id)
    cancelled = service.create_schedule("REMINDER", {"datetime": future(), "text": "x"})
    service.cancel_schedule(cancelled.id, "REMINDER")
    active = service.create_schedule("REMINDER", {"datetime": future(), "text": "y"})
    due = active.next_run_at
    user.is_active = False
    session.commit()
    assert tick(session, due + timedelta(seconds=1)) == 0
    user.is_active = True
    session.commit()
    assert tick(session, due + timedelta(seconds=1)) == 1


# Documentação: Verifica o cenário
# test_cancel_invalidates_pending_outbox_and_deduplicates_call_cancel; as condições e resultados
# esperados aparecem nos asserts.
def test_cancel_invalidates_pending_outbox_and_deduplicates_call_cancel(session, user):
    service = PlanningService(session, user.id)
    row = service.create_schedule("CALL", {"datetime": future()})
    due = row.next_run_at
    session.commit()
    tick(session, due)
    service.cancel_schedule(row.id, "CALL")
    session.commit()
    service.cancel_schedule(row.id, "CALL")
    session.commit()
    incoming = session.scalar(select(OutboxEvent).where(OutboxEvent.type == "call.incoming"))
    assert incoming.status == "CANCELLED"
    assert (
        session.scalar(
            select(func.count())
            .select_from(OutboxEvent)
            .where(OutboxEvent.type == "call.cancelled")
        )
        == 1
    )


# Documentação: Verifica o cenário test_action_savepoint_isolates_failure_and_success; as
# condições e resultados esperados aparecem nos asserts.
def test_action_savepoint_isolates_failure_and_success(session, user):
    _, messages = history(session, user, ["Criar tarefa e cancelar lembrete"])
    actions = [
        ActionProposal(type="cancel_reminder", arguments={"id": str(uuid4())}),
        ActionProposal(type="create_task", arguments={"title": "Preservada"}),
    ]
    results = ActionEngine(session).process(actions, messages[0])
    session.commit()
    assert [row["status"] for row in results] == ["FAILED", "SUCCEEDED"]
    assert session.scalar(select(Task)).title == "Preservada"
