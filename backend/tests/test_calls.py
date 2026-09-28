from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from test_devices import authenticate, envelope, receive

from app.agent.errors import AgentError
from app.calls.service import CallService
from app.db.session import get_engine
from app.devices.service import pending, register
from app.models import CallSession, Conversation, OutboxEvent, User


# Documentação: Implementa ringing como parte do fluxo descrito para este arquivo.
def ringing(session, user, age=0):
    event = OutboxEvent(
        user_id=user.id,
        type="call.incoming",
        payload={"text": "coffee talk"},
        dedupe_key=str(uuid4()),
        created_at=datetime.now(UTC) - timedelta(seconds=age),
    )
    session.add(event)
    session.commit()
    return event


# Documentação: Verifica o cenário test_answer_creates_once_and_end_is_idempotent; as condições e
# resultados esperados aparecem nos asserts.
def test_answer_creates_once_and_end_is_idempotent(session, user):
    device = uuid4()
    register(session, device, user.id)
    session.commit()
    event = ringing(session, user)
    service = CallService(session, user.id, device)
    first = service.answer(event.id)
    session.commit()
    assert service.answer(event.id) == first
    assert session.scalar(select(func.count()).select_from(CallSession)) == 1
    assert session.scalar(select(func.count()).select_from(Conversation)) == 1
    assert event.status == "CANCELLED"
    assert service.touch(UUID(first["id"])) == UUID(first["conversation_id"])
    session.commit()
    ended = service.end(UUID(first["id"]))
    session.commit()
    assert ended["status"] == "ENDED"
    assert service.end(UUID(first["id"])) == ended
    with pytest.raises(AgentError, match="call_not_active"):
        service.touch(UUID(first["id"]))


# Documentação: Verifica o cenário test_concurrent_devices_cannot_both_answer; as condições e
# resultados esperados aparecem nos asserts.
def test_concurrent_devices_cannot_both_answer(session, user):
    devices = [uuid4(), uuid4()]
    for device in devices:
        register(session, device, user.id)
    session.commit()
    event = ringing(session, user)

    # Documentação: Implementa test_concurrent_devices_cannot_both_answer.answer como parte do
    # fluxo descrito para este arquivo.
    def answer(device):
        with Session(get_engine(), expire_on_commit=False) as db:
            try:
                result = CallService(db, user.id, device).answer(event.id)
                db.commit()
                return result["id"]
            except AgentError as error:
                db.rollback()
                return error.code

    with ThreadPoolExecutor(max_workers=2) as pool:
        result = list(pool.map(answer, devices))
    assert result.count("call_answered_on_another_device") == 1
    assert session.scalar(select(func.count()).select_from(CallSession)) == 1


# Documentação: Verifica o cenário test_reject_expiry_and_other_owner; as condições e resultados
# esperados aparecem nos asserts.
def test_reject_expiry_and_other_owner(session, user):
    device = uuid4()
    register(session, device, user.id)
    session.commit()
    event = ringing(session, user)
    service = CallService(session, user.id, device)
    assert service.reject(event.id)["status"] == "REJECTED"
    session.commit()
    assert service.reject(event.id)["status"] == "REJECTED"
    with pytest.raises(AgentError, match="call_no_longer_ringing"):
        service.answer(event.id)
    session.rollback()
    old = ringing(session, user, age=121)
    frames = pending(session, user.id, device)
    session.refresh(old)
    assert old.status == "CANCELLED"
    assert not any(frame["event_id"] == str(old.id) for frame in frames)
    assert any(
        frame["type"] == "call.dismissed" and frame["payload"]["status"] == "MISSED"
        for frame in frames
    )
    other = User(username="other-call", password_hash=user.password_hash, timezone=user.timezone)
    session.add(other)
    session.commit()
    with pytest.raises(AgentError, match="call_not_found"):
        CallService(session, other.id).incoming(event.id)


# Documentação: Verifica o cenário test_idle_call_expires_and_foreign_device_cannot_end; as
# condições e resultados esperados aparecem nos asserts.
def test_idle_call_expires_and_foreign_device_cannot_end(session, user):
    device, other = uuid4(), uuid4()
    register(session, device, user.id)
    register(session, other, user.id)
    session.commit()
    event = ringing(session, user)
    service = CallService(session, user.id, device)
    answered = service.answer(event.id)
    session.commit()
    with pytest.raises(AgentError, match="call_device_mismatch"):
        CallService(session, user.id, other).end(UUID(answered["id"]))
    session.rollback()
    service.expire(datetime.now(UTC) + timedelta(minutes=11))
    session.commit()
    assert session.get(CallSession, UUID(answered["id"])).status == "EXPIRED"


# Documentação: Verifica o cenário test_http_device_session_bound_and_owner_guards; as condições e
# resultados esperados aparecem nos asserts.
def test_http_device_session_bound_and_owner_guards(client, session, user):
    device = uuid4()
    event = ringing(session, user)
    response = client.post(
        "/auth/login",
        json={
            "username": user.username,
            "password": "test-password-only",
            "device_id": str(device),
        },
    )
    auth = {"Authorization": "Bearer " + response.json()["access_token"]}
    assert (
        client.post(
            f"/calls/incoming/{event.id}/answer", headers=auth, json={"device_id": str(uuid4())}
        ).status_code
        == 403
    )
    result = client.post(
        f"/calls/incoming/{event.id}/answer", headers=auth, json={"device_id": str(device)}
    )
    assert result.status_code == 200
    assert client.get("/calls", headers=auth).json()[0]["id"] == result.json()["id"]
    assert (
        client.post(
            f"/calls/{result.json()['id']}/end", headers=auth, json={"device_id": str(device)}
        ).json()["status"]
        == "ENDED"
    )
    assert (
        client.post(
            f"/calls/incoming/{event.id}/host_shell", headers=auth, json={"device_id": str(device)}
        ).status_code
        == 404
    )


# Documentação: Verifica o cenário test_websocket_call_answer_reject_end_are_durable; as condições
# e resultados esperados aparecem nos asserts.
def test_websocket_call_answer_reject_end_are_durable(client, session, user):
    event = ringing(session, user)
    with client.websocket_connect("/ws") as ws:
        authenticate(ws, user)
        receive(ws, "call.incoming")
        ws.send_json(envelope("call.answer", {"incoming_event_id": str(event.id)}))
        result = receive(ws, "call.command_result")["payload"]["result"]
        assert result["status"] == "ACTIVE"
        persisted = receive(ws, "call.state")
        assert persisted["payload"]["session"]["id"] == result["id"]
        ws.send_json(envelope("call.end", {"call_session_id": result["id"]}))
        assert receive(ws, "call.command_result")["payload"]["result"]["status"] == "ENDED"
    assert session.scalar(select(CallSession)).status == "ENDED"


# Documentação: Verifica o cenário test_voice_turn_replay_and_next_turn_keep_call_context; as
# condições e resultados esperados aparecem nos asserts.
def test_voice_turn_replay_and_next_turn_keep_call_context(client, session, user, monkeypatch):
    from contextlib import contextmanager

    from test_context import StubRouter

    import app.api.websocket as websocket_module
    from app.agent.core import AgentCore

    stub = StubRouter(*[{"reply": "Resposta de voz", "actions": [], "memory_candidates": []}] * 2)

    @contextmanager
    # Documentação: Implementa test_voice_turn_replay_and_next_turn_keep_call_context.factory como
    # parte do fluxo descrito para este arquivo.
    def factory(*_):
        yield stub

    monkeypatch.setattr(
        websocket_module,
        "AgentCore",
        lambda db, settings: AgentCore(db, settings, router_factory=factory),
    )
    event = ringing(session, user)
    with client.websocket_connect("/ws") as ws:
        authenticate(ws, user)
        ws.send_json(envelope("call.answer", {"incoming_event_id": str(event.id)}))
        call = receive(ws, "call.command_result")["payload"]["result"]
        identifier = uuid4()
        request = envelope(
            "voice.transcript",
            {
                "call_session_id": call["id"],
                "client_message_id": str(identifier),
                "content": "Olá por voz",
            },
            identifier,
        )
        ws.send_json(request)
        reply = receive(ws, "agent.message")
        assert reply["payload"]["conversation_id"] == call["conversation_id"]
        ws.send_json(envelope("event.ack", {"event_id": reply["event_id"]}))
        receive(ws, "event.acknowledged")
        ws.send_json(request)
        while not receive(ws, "chat.processed")["payload"]["replayed"]:
            pass
        assert len(stub.calls) == 1
        second = uuid4()
        ws.send_json(
            envelope(
                "voice.transcript",
                {
                    "call_session_id": call["id"],
                    "client_message_id": str(second),
                    "content": "Continue a conversa",
                },
                second,
            )
        )
        assert receive(ws, "agent.message")["payload"]["conversation_id"] == call["conversation_id"]
        assert len(stub.calls) == 2
