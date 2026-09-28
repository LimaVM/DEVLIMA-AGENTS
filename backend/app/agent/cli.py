"""Real local inference against isolated, ephemeral test data only."""

import argparse
import json
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.agent.core import AgentCore
from app.config import get_settings
from app.db.session import get_engine
from app.models import ConversationSummary, LLMRequest, Memory, Message, User
from app.schemas.chat import ChatSend
from app.security import hash_password


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["smoke", "verify"])
    args = parser.parse_args()
    settings = get_settings()
    if (
        settings.postgres_host != "postgres-test"
        or settings.postgres_db != "devlima_agent_test"
        or settings.allow_cloud_fallback
    ):
        raise SystemExit("Smoke exige banco de teste isolado e fallback cloud desligado")
    if args.command == "verify":
        verify_persistence(settings)
        return
    with Session(get_engine(), expire_on_commit=False) as session:
        user = User(
            username=f"smoke-{uuid4().hex[:20]}",
            password_hash=hash_password(uuid4().hex),
            timezone="America/Sao_Paulo",
            is_active=False,
        )
        session.add(user)
        session.commit()
        core = AgentCore(session, settings)
        first = ChatSend(
            client_message_id=uuid4(), content="Lembre que eu prefiro respostas curtas."
        )
        replies = [core.send(user.id, first)]
        conversation_id = replies[0].conversation_id
        for phrase in (
            "Qual preferência sobre respostas você acabou de guardar?",
            "O que você sabe sobre minha preferência?",
        ):
            replies.append(
                core.send(
                    user.id,
                    ChatSend(
                        conversation_id=conversation_id, client_message_id=uuid4(), content=phrase
                    ),
                )
            )
        attempts_before = session.scalar(
            select(func.count()).select_from(LLMRequest).where(LLMRequest.user_id == user.id)
        )
        replay = core.send(user.id, first)
        attempts_after = session.scalar(
            select(func.count()).select_from(LLMRequest).where(LLMRequest.user_id == user.id)
        )
        assert replay.replayed and attempts_before == attempts_after
        # A new session/Core retrieves the same database memory in a new conversation.
        user_id = user.id
    with Session(get_engine(), expire_on_commit=False) as session:
        cross = AgentCore(session, settings).send(
            user_id, ChatSend(client_message_id=uuid4(), content="Como prefiro que você responda?")
        )
        memories = session.scalar(
            select(func.count())
            .select_from(Memory)
            .where(Memory.user_id == user_id, Memory.is_active.is_(True))
        )
        summaries = session.scalar(
            select(func.count())
            .select_from(ConversationSummary)
            .where(ConversationSummary.user_id == user_id)
        )
        raw_messages = session.scalar(
            select(func.count()).select_from(Message).where(Message.user_id == user_id)
        )
        cloud_attempts = session.scalar(
            select(func.count())
            .select_from(LLMRequest)
            .where(LLMRequest.user_id == user_id, LLMRequest.provider == "groq")
        )
        assert memories >= 1 and summaries >= 1 and raw_messages == 8 and cloud_attempts == 0
        assert cross.context_stats["memory_count"] >= 1
        print(
            json.dumps(
                {
                    "status": "ok",
                    "provider": cross.provider,
                    "cloud_attempts": cloud_attempts,
                    "memories": memories,
                    "summaries": summaries,
                    "raw_messages": raw_messages,
                    "idempotent_replay": replay.replayed,
                    "new_session_memory_count": cross.context_stats["memory_count"],
                    "turns": [
                        {
                            "reply": row.reply,
                            "latency_ms": row.latency_ms,
                            "context": row.context_stats,
                        }
                        for row in [*replies, cross]
                    ],
                },
                ensure_ascii=False,
            )
        )


def verify_persistence(settings):
    with Session(get_engine(), expire_on_commit=False) as session:
        user = session.scalar(
            select(User)
            .where(User.username.startswith("smoke-"), User.is_active.is_(False))
            .order_by(User.created_at.desc())
            .limit(1)
        )
        if user is None:
            raise SystemExit("Execute smoke antes de verify")
        source = session.scalar(
            select(Message)
            .where(Message.user_id == user.id, Message.role == "user")
            .order_by(Message.created_at, Message.id)
            .limit(1)
        )
        before = session.scalar(
            select(func.count()).select_from(LLMRequest).where(LLMRequest.user_id == user.id)
        )
        result = AgentCore(session, settings).send(
            user.id,
            ChatSend(
                content=source.content,
                client_message_id=source.client_message_id,
                conversation_id=source.conversation_id,
            ),
        )
        after = session.scalar(
            select(func.count()).select_from(LLMRequest).where(LLMRequest.user_id == user.id)
        )
        messages = session.scalar(
            select(func.count()).select_from(Message).where(Message.user_id == user.id)
        )
        summaries = session.scalar(
            select(func.count())
            .select_from(ConversationSummary)
            .where(ConversationSummary.user_id == user.id)
        )
        memories = session.scalar(
            select(func.count())
            .select_from(Memory)
            .where(Memory.user_id == user.id, Memory.is_active.is_(True))
        )
        assert (
            result.replayed
            and before == after
            and messages == 8
            and summaries >= 1
            and memories >= 1
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "new_process_replay": result.replayed,
                    "new_llm_requests": after - before,
                    "raw_messages": messages,
                    "summaries": summaries,
                    "memories": memories,
                }
            )
        )


if __name__ == "__main__":
    main()
