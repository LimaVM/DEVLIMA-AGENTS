import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from threading import Event
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.agent.action_parser import MemoryProposal, SummaryEnvelope, parse_response
from app.agent.context_builder import ContextBuilder
from app.agent.core import AgentCore
from app.agent.errors import AgentError, InvalidAgentResponse
from app.agent.memory_manager import MemoryManager
from app.config import get_settings
from app.db.session import get_engine
from app.llm.base import LLMCompletion, LLMError
from app.llm.router import RoutedCompletion
from app.models import (
    AgentAction,
    AuditLog,
    Conversation,
    ConversationSummary,
    Memory,
    Message,
    User,
)
from app.schemas.chat import ChatSend
from app.security import create_token


class StubRouter:
    def __init__(self, *outputs):
        self.outputs = list(outputs) or [{"reply": "Olá", "actions": [], "memory_candidates": []}]
        self.calls = []

    def chat(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        output = self.outputs.pop(0)
        if isinstance(output, Exception):
            raise output
        return RoutedCompletion(
            request_id=uuid4(),
            completion=LLMCompletion(
                content=output if isinstance(output, str) else json.dumps(output),
                provider="llama_cpp",
                model="test",
            ),
            fallback_used=False,
            latency_ms=1,
        )

    @contextmanager
    def factory(self, settings, session):
        yield self


def send(core, user, content="Olá", conversation_id=None, identifier=None):
    return core.send(
        user.id,
        ChatSend(
            content=content,
            conversation_id=conversation_id,
            client_message_id=identifier or uuid4(),
        ),
    )


def history(session, user, texts):
    conversation = Conversation(user_id=user.id, title="Contexto", last_sequence=len(texts))
    session.add(conversation)
    session.flush()
    rows = []
    for index, content in enumerate(texts, 1):
        row = Message(
            user_id=user.id,
            conversation_id=conversation.id,
            sequence=index,
            role="user" if index % 2 else "assistant",
            content=content,
            status="COMPLETED",
            info={},
        )
        session.add(row)
        rows.append(row)
    session.commit()
    return conversation, rows


@pytest.mark.parametrize(
    "raw",
    [
        '{"reply":"a","reply":"b"}',
        '```json\n{"reply":"a"}\n```',
        "[]",
        '{"reply":"   "}',
        '{"reply":"a","shell":"ls"}',
        '{"reply":"a","actions":[{"type":"shell","arguments":{"command":"ls"}}]}',
        '{"reply":"a","actions":[{"type":"destroy_worker","arguments":{"worker_id":"/etc/passwd"}}]}',
        '{"reply":"a","actions":[{"type":"create_reminder","arguments":{"text":"x","datetime":"2026-09-28T10:00:00"}}]}',
        '{"reply":"a","memory_candidates":[{"content":"x","category":"fact","confidence":2}]}',
    ],
)
def test_untrusted_envelope_rejected(raw):
    with pytest.raises(InvalidAgentResponse):
        parse_response(raw)


def test_action_datetime_normalized_and_limits():
    result = parse_response(
        json.dumps(
            {
                "reply": "a",
                "actions": [
                    {
                        "type": "create_reminder",
                        "arguments": {"text": "Teste", "datetime": "2026-09-28T10:00:00-03:00"},
                    }
                ],
            }
        )
    )
    assert result.actions[0].arguments["datetime"] == "2026-09-28T13:00:00Z"
    with pytest.raises(InvalidAgentResponse):
        parse_response(
            json.dumps(
                {
                    "reply": "a",
                    "actions": [{"type": "create_linux_worker", "arguments": {"vcpu": 99}}],
                }
            )
        )
    with pytest.raises(InvalidAgentResponse):
        parse_response(json.dumps({"summary": "x", "facts": ["x" * 161]}), SummaryEnvelope)


@pytest.mark.parametrize(
    "source_text,content,confidence,status",
    [
        ("Lembre que prefiro café.", "prefiro café", 0.95, "ACCEPTED"),
        ("Prefiro respostas curtas.", "Prefiro respostas curtas", 0.95, "ACCEPTED"),
        ("Gosto de café", "Gosto de café", 0.95, "PENDING"),
        ("Lembre que prefiro café", "prefiro chá", 0.99, "PENDING"),
        ("Lembre que prefiro café", "prefiro café", 0.5, "PENDING"),
        ("Lembre que token=secret123456", "token=secret123456", 0.99, "REJECTED"),
    ],
)
def test_memory_requires_explicit_grounded_confidence(
    session, user, source_text, content, confidence, status
):
    _, rows = history(session, user, [source_text])
    manager = MemoryManager(session, user.id)
    candidate = manager.consider(
        MemoryProposal(content=content, category="preference", confidence=confidence), rows[0]
    )
    session.commit()
    assert candidate.status == status
    assert session.scalar(select(func.count()).select_from(Memory)) == int(status == "ACCEPTED")
    if status == "REJECTED":
        assert "secret123456" not in candidate.content
        with pytest.raises(AgentError, match="candidate_rejected"):
            manager.accept(candidate.id)


def test_pending_confirmation_dedup_deactivate(session, user):
    _, rows = history(session, user, ["Eu gosto de café"])
    manager = MemoryManager(session, user.id)
    candidate = manager.consider(
        MemoryProposal(content="gosto de café", category="fact", confidence=0.95), rows[0]
    )
    memory = manager.accept(candidate.id)
    session.commit()
    assert manager.accept(candidate.id).id == memory.id
    assert manager.create("GOSTO DE CAFÉ.", "fact").id == memory.id
    memory.is_active = False
    session.commit()
    assert manager.relevant("café") == []
    with pytest.raises(AgentError, match="memory_no_longer_active"):
        manager.accept(candidate.id)


def test_context_bounds_timezone_and_original_history(session, user):
    conversation, rows = history(session, user, [f"{i}:" + "x" * 3990 for i in range(20)])
    current = Message(
        user_id=user.id,
        conversation_id=conversation.id,
        sequence=21,
        role="user",
        content="pergunta atual",
        status="PENDING",
        info={},
    )
    session.add(current)
    session.commit()
    manager = MemoryManager(session, user.id)
    manager.create("Prefiro respostas curtas", "preference")
    session.commit()
    context = ContextBuilder(session, get_settings()).build(user, conversation, current)
    assert context.stats["context_chars"] <= 12000
    assert context.stats["history_messages_sent"] <= 8
    assert context.stats["history_messages_stored"] == 20
    assert context.messages[-1].content == current.content
    system = context.messages[0].content
    assert "America/Sao_Paulo" in system and "-03:00" in system and "now_utc" in system
    assert rows[0].content.endswith("x" * 3990)
    assert session.scalar(select(func.count()).select_from(Message)) == 21


def test_core_persistence_replay_and_key_conflict(session, user):
    stub = StubRouter()
    core = AgentCore(session, get_settings(), stub.factory)
    identifier = uuid4()
    reply = send(core, user, identifier=identifier)
    with Session(get_engine(), expire_on_commit=False) as fresh:
        same = send(AgentCore(fresh, get_settings(), stub.factory), user, identifier=identifier)
    assert same.replayed and same.assistant_message_id == reply.assistant_message_id
    assert len(stub.calls) == 1
    assert session.scalar(select(func.count()).select_from(Message)) == 2
    with pytest.raises(AgentError, match="idempotency_key_conflict"):
        send(core, user, content="Diferente", identifier=identifier)


@pytest.mark.parametrize(
    "failure",
    [LLMError("timeout"), '{"reply": "bad", "actions":[{"type":"shell","arguments":{}}]}'],
)
def test_failed_user_message_survives_and_can_retry(session, user, failure):
    stub = StubRouter(failure, {"reply": "Funcionou"})
    core = AgentCore(session, get_settings(), stub.factory)
    identifier = uuid4()
    with pytest.raises((LLMError, InvalidAgentResponse)):
        send(core, user, identifier=identifier)
    source = session.scalar(select(Message))
    conversation = session.get(Conversation, source.conversation_id)
    assert source.status == "FAILED" and source.content == "Olá"
    assert conversation.lease_owner is None and conversation.pending_message_id is None
    result = send(core, user, identifier=identifier)
    assert result.user_message_id == source.id and result.reply == "Funcionou"
    assert session.scalar(select(func.count()).select_from(Message)) == 2
    assert len(stub.calls) == 2


def test_failed_old_turn_cannot_be_inserted_out_of_order(session, user):
    stub = StubRouter(LLMError("timeout"), {"reply": "nova"})
    core = AgentCore(session, get_settings(), stub.factory)
    identifier = uuid4()
    with pytest.raises(LLMError):
        send(core, user, identifier=identifier)
    conversation = session.scalar(select(Conversation))
    send(core, user, content="Nova pergunta", conversation_id=conversation.id)
    with pytest.raises(AgentError, match="failed_turn_not_latest"):
        send(core, user, identifier=identifier)


def test_action_is_validated_recorded_but_unavailable(session, user):
    stub = StubRouter(
        {
            "reply": "Tarefa criada",
            "actions": [{"type": "create_task", "arguments": {"title": "Teste"}}],
        }
    )
    reply = send(AgentCore(session, get_settings(), stub.factory), user, content="Crie uma tarefa")
    assert "não consigo executar" in reply.reply
    assert reply.actions[0]["status"] == "UNSUPPORTED"
    assert session.scalar(select(AgentAction)).arguments == {"title": "Teste"}
    assert session.scalar(select(AuditLog).where(AuditLog.event == "agent.action_unavailable"))


def test_duplicate_proposals_and_pending_feedback(session, user):
    proposal = {"content": "gosto de café", "category": "fact", "confidence": 0.95}
    stub = StubRouter({"reply": "Entendi", "memory_candidates": [proposal, proposal]})
    reply = send(AgentCore(session, get_settings(), stub.factory), user, content="Eu gosto de café")
    assert len(reply.memory_candidates) == 1 and reply.memory_candidates[0]["status"] == "PENDING"
    assert "aguardando sua confirmação" in reply.reply
    assert session.scalar(select(func.count()).select_from(Memory)) == 0


def test_summary_keeps_raw_history_and_recent_pair(session, user):
    settings = get_settings().model_copy(
        update={"context_recent_messages": 2, "summary_trigger_messages": 4}
    )
    conversation, rows = history(
        session, user, ["nome Guilherme", "Olá", "prefiro curtas", "entendi"]
    )
    stub = StubRouter(
        {
            "summary": "Usuário Guilherme prefere respostas curtas",
            "facts": ["Prefere respostas curtas"],
            "open_topics": [],
        },
        {"reply": "Oi Guilherme"},
    )
    reply = send(
        AgentCore(session, settings, stub.factory),
        user,
        content="Como me chamo?",
        conversation_id=conversation.id,
    )
    summary = session.scalar(select(ConversationSummary))
    assert summary.through_sequence == 2
    assert reply.context_stats["summary_through_sequence"] == 2
    assert [message.content for message in stub.calls[-1][0][1:]] == [
        rows[2].content,
        rows[3].content,
        "Como me chamo?",
    ]
    assert session.scalar(select(func.count()).select_from(Message)) == 6


@pytest.mark.parametrize("summary_failure", [LLMError("timeout"), "not json"])
def test_optional_summary_failure_preserves_chat(session, user, summary_failure):
    settings = get_settings().model_copy(
        update={"context_recent_messages": 2, "summary_trigger_messages": 4}
    )
    conversation, _ = history(session, user, ["a", "b", "c", "d"])
    stub = StubRouter(summary_failure, {"reply": "Resposta"})
    result = send(AgentCore(session, settings, stub.factory), user, conversation_id=conversation.id)
    assert result.reply == "Resposta"
    assert session.scalar(select(func.count()).select_from(ConversationSummary)) == 0
    assert session.scalar(select(AuditLog).where(AuditLog.event == "summary.failed"))


def test_concurrent_turn_busy_without_duplicate_provider(session, user):
    conversation, _ = history(session, user, [])
    entered, release = Event(), Event()

    class BlockingRouter(StubRouter):
        def chat(self, messages, **kwargs):
            entered.set()
            assert release.wait(10)
            return super().chat(messages, **kwargs)

    stub = BlockingRouter()

    def first():
        with Session(get_engine(), expire_on_commit=False) as independent:
            return send(
                AgentCore(independent, get_settings(), stub.factory),
                user,
                conversation_id=conversation.id,
            )

    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(first)
        try:
            assert entered.wait(10)
            with pytest.raises(AgentError, match="conversation_busy"):
                send(
                    AgentCore(session, get_settings(), StubRouter().factory),
                    user,
                    conversation_id=conversation.id,
                )
        finally:
            session.rollback()
            release.set()
        assert pending.result(timeout=10).reply == "Olá"
    assert len(stub.calls) == 1
    assert session.scalar(select(func.count()).select_from(Message)) == 2


def test_expired_lease_recovers_and_stale_owner_cannot_release(session, user):
    core = AgentCore(session, get_settings(), StubRouter().factory)
    lease = uuid4()
    conversation, source = core._claim(
        user.id, ChatSend(content="pergunta antiga", client_message_id=uuid4()), lease
    )
    conversation.lease_until = datetime.now(UTC) - timedelta(seconds=1)
    session.commit()
    fresh_lease = uuid4()
    _, new_source = core._claim(
        user.id,
        ChatSend(
            content="pergunta nova", conversation_id=conversation.id, client_message_id=uuid4()
        ),
        fresh_lease,
    )
    assert source.status == "FAILED" and source.error_code == "processing_lease_expired"
    core._fail(conversation.id, source.id, lease, "timeout")
    session.refresh(conversation)
    assert (
        conversation.lease_owner == fresh_lease and conversation.pending_message_id == new_source.id
    )


def test_api_auth_tenant_isolation_and_memory_lifecycle(client, session, user):
    headers = {"Authorization": f"Bearer {create_token(user, get_settings())}"}
    assert client.get("/chat/conversations").status_code == 401
    assert client.get("/memories").status_code == 401
    conversation, rows = history(session, user, ["gosto de café"])
    manager = MemoryManager(session, user.id)
    candidate = manager.consider(
        MemoryProposal(content="gosto de café", category="fact", confidence=0.95), rows[0]
    )
    other = User(username="other", password_hash=user.password_hash, timezone=user.timezone)
    session.add(other)
    session.commit()
    other_headers = {"Authorization": f"Bearer {create_token(other, get_settings())}"}
    assert (
        client.get(
            f"/chat/conversations/{conversation.id}/messages", headers=other_headers
        ).status_code
        == 404
    )
    assert (
        client.post(
            f"/memories/candidates/{candidate.id}/accept", headers=other_headers
        ).status_code
        == 404
    )
    assert client.get("/memories/candidates", headers=other_headers).json() == []
    assert (
        client.post(
            "/chat/messages",
            headers=other_headers,
            json={
                "conversation_id": str(conversation.id),
                "client_message_id": str(uuid4()),
                "content": "oi",
            },
        ).status_code
        == 404
    )
    accepted = client.post(f"/memories/candidates/{candidate.id}/accept", headers=headers)
    assert accepted.status_code == 200
    identifier = accepted.json()["id"]
    assert client.delete(f"/memories/{identifier}", headers=other_headers).status_code == 404
    assert client.delete(f"/memories/{identifier}", headers=headers).status_code == 204
    assert client.get("/memories", headers=headers).json() == []
    assert (
        client.post(f"/memories/candidates/{candidate.id}/accept", headers=headers).status_code
        == 409
    )
    assert (
        client.post(
            "/memories", headers=headers, json={"content": "token=secret123456", "category": "fact"}
        ).status_code
        == 422
    )
    assert (
        client.post(f"/chat/conversations/{conversation.id}/archive", headers=headers).status_code
        == 204
    )
    assert (
        len(client.get(f"/chat/conversations/{conversation.id}/messages", headers=headers).json())
        == 1
    )
    assert client.get("/chat/conversations", headers=headers).json() == []
    assert len(client.get("/chat/conversations?archived=true", headers=headers).json()) == 1
    assert (
        client.post(
            "/chat/messages",
            headers=headers,
            json={
                "conversation_id": str(conversation.id),
                "client_message_id": str(uuid4()),
                "content": "oi",
            },
        ).json()["detail"]
        == "conversation_archived"
    )


def test_context_memory_owner_isolation(session, user):
    other = User(username="other", password_hash=user.password_hash, timezone=user.timezone)
    session.add(other)
    session.commit()
    MemoryManager(session, other.id).create("Prefiro informação privada", "preference")
    conversation, rows = history(session, user, ["privada"])
    context = ContextBuilder(session, get_settings()).build(user, conversation, rows[0])
    assert context.stats["memory_count"] == 0
    assert "informação privada" not in context.messages[0].content
    with pytest.raises(ValueError, match="ownership"):
        ContextBuilder(session, get_settings()).build(other, conversation, rows[0])


def test_api_reject_candidate_and_pagination(client, session, user):
    conversation, rows = history(session, user, ["a", "b", "c", "d"])
    candidate = MemoryManager(session, user.id).consider(
        MemoryProposal(content="prefiro curtas", category="preference", confidence=0.8), rows[0]
    )
    session.commit()
    headers = {"Authorization": f"Bearer {create_token(user, get_settings())}"}
    response = client.get(
        f"/chat/conversations/{conversation.id}/messages?after_sequence=2&limit=1", headers=headers
    )
    assert response.status_code == 200 and response.json()[0]["sequence"] == 3
    assert client.get("/memories/candidates?status=unknown", headers=headers).status_code == 422
    assert (
        client.post(f"/memories/candidates/{candidate.id}/reject", headers=headers).status_code
        == 204
    )
    assert (
        client.post(f"/memories/candidates/{candidate.id}/accept", headers=headers).status_code
        == 409
    )
    assert (
        client.post("/chat/conversations", headers=headers, json={"title": "Nova"}).status_code
        == 201
    )


def test_api_chat_response_replay_and_failure(client, session, user, monkeypatch):
    stub = StubRouter({"reply": "Resposta humana"}, LLMError("timeout"))
    monkeypatch.setattr(
        "app.api.chat.AgentCore", lambda db, settings: AgentCore(db, settings, stub.factory)
    )
    headers = {"Authorization": f"Bearer {create_token(user, get_settings())}"}
    payload = {"client_message_id": str(uuid4()), "content": "Oi"}
    first = client.post("/chat/messages", json=payload, headers=headers)
    assert first.status_code == 200 and first.json()["reply"] == "Resposta humana"
    assert not first.json()["replayed"]
    assert client.post("/chat/messages", json=payload, headers=headers).json()["replayed"]
    payload["client_message_id"] = str(uuid4())
    payload["conversation_id"] = first.json()["conversation_id"]
    failed = client.post("/chat/messages", json=payload, headers=headers)
    assert failed.status_code == 503 and failed.json()["detail"] == "timeout"
    assert session.scalar(select(Message).where(Message.status == "FAILED")).content == "Oi"


def test_context_low_budget_long_message_and_summary(session, user):
    conversation, rows = history(session, user, ["a", "b"])
    session.add(
        ConversationSummary(
            user_id=user.id,
            conversation_id=conversation.id,
            through_sequence=2,
            content={
                "summary": "r" * 1800,
                "facts": ["f" * 160] * 8,
                "open_topics": ["t" * 160] * 8,
            },
        )
    )
    current = Message(
        user_id=user.id,
        conversation_id=conversation.id,
        sequence=3,
        role="user",
        content="x" * 4000,
        status="PENDING",
        info={},
    )
    session.add(current)
    for index in range(5):
        MemoryManager(session, user.id).create(f"Prefiro {index}" + "m" * 980, "preference")
    session.commit()
    settings = get_settings().model_copy(update={"context_max_chars": 10000})
    context = ContextBuilder(session, settings).build(user, conversation, current)
    assert context.stats["context_chars"] <= 10000
    assert context.messages[-1].content == "x" * 4000
    assert len(context.messages[0].content) <= 8000


def test_archive_busy_and_expired_turn_revokes_old_lease(client, session, user):
    core = AgentCore(session, get_settings(), StubRouter().factory)
    lease = uuid4()
    conversation, source = core._claim(
        user.id, ChatSend(content="turno abandonado", client_message_id=uuid4()), lease
    )
    headers = {"Authorization": f"Bearer {create_token(user, get_settings())}"}
    url = f"/chat/conversations/{conversation.id}/archive"
    assert client.post(url, headers=headers).status_code == 409
    conversation.lease_until = datetime.now(UTC) - timedelta(seconds=1)
    session.commit()
    assert client.post(url, headers=headers).status_code == 204
    session.refresh(conversation)
    session.refresh(source)
    assert conversation.archived and conversation.lease_owner is None
    assert source.status == "FAILED" and source.content == "turno abandonado"
