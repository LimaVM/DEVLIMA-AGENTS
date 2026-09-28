"""Real cloud fallback smoke with synthetic data, restricted to the test database."""

import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.agent.core import AgentCore
from app.config import get_settings
from app.db.session import get_engine
from app.models import LLMRequest, OutboxEvent, Schedule, Task, User
from app.planning.scheduler import tick
from app.schemas.chat import ChatSend
from app.security import hash_password


# Documentação: Coordena a entrada de linha de comando deste arquivo: Executa smoke de tarefas,
# lembretes, recorrência e scheduler usando registros isolados para validar APIs e persistência.
def main():
    settings = get_settings()
    if (
        settings.postgres_host != "postgres-test"
        or settings.postgres_db != "devlima_agent_test"
        or not settings.allow_cloud_fallback
        or settings.local_llm_base_url != "http://127.0.0.1:9/v1"
    ):
        raise SystemExit("Planning smoke exige banco de teste e falha local isolada")
    with Session(get_engine(), expire_on_commit=False) as session:
        user = User(
            username=f"planning-{uuid4().hex[:20]}",
            password_hash=hash_password(uuid4().hex),
            timezone="America/Sao_Paulo",
            is_active=True,
        )
        session.add(user)
        session.commit()
        core = AgentCore(session, settings)
        task_request = ChatSend(
            client_message_id=uuid4(),
            content="Crie uma tarefa com o título Teste isolado do agendamento. Use create_task.",
        )
        task_reply = core.send(user.id, task_request)
        when = datetime.now(UTC) + timedelta(minutes=5)
        reminder_request = ChatSend(
            conversation_id=task_reply.conversation_id,
            client_message_id=uuid4(),
            content=(
                f"Crie um lembrete para tomar café exatamente em {when.isoformat()}. "
                "Use create_reminder."
            ),
        )
        reminder_reply = core.send(user.id, reminder_request)
        task_count = session.scalar(
            select(func.count()).select_from(Task).where(Task.user_id == user.id)
        )
        schedule = session.scalar(
            select(Schedule).where(Schedule.user_id == user.id, Schedule.kind == "REMINDER")
        )
        assert task_count == 1 and schedule is not None
        source_id = reminder_reply.user_message_id
        replay = core.send(user.id, reminder_request)
        assert replay.replayed and replay.user_message_id == source_id
        due = schedule.next_run_at
        assert tick(session, due + timedelta(seconds=1)) == 1
        assert tick(session, due + timedelta(seconds=2)) == 0
        event = session.scalar(
            select(OutboxEvent).where(
                OutboxEvent.user_id == user.id, OutboxEvent.type == "reminder.triggered"
            )
        )
        assert event is not None
        attempts = session.scalars(
            select(LLMRequest).where(LLMRequest.user_id == user.id).order_by(LLMRequest.created_at)
        ).all()
        assert task_reply.fallback_used and reminder_reply.fallback_used
        assert len(attempts) == 4 and sum(row.provider == "groq" for row in attempts) == 2
        print(
            json.dumps(
                {
                    "status": "ok",
                    "tasks": task_count,
                    "schedule_created": True,
                    "replay": replay.replayed,
                    "outbox_type": event.type,
                    "outbox_event_id": str(event.id),
                    "groq_attempts": 2,
                    "local_error_codes": [
                        row.error_code for row in attempts if row.provider == "llama_cpp"
                    ],
                    "replies": [task_reply.reply, reminder_reply.reply],
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
