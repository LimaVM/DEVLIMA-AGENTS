import json
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy import func, select
from test_context import StubRouter
from test_planning import headers

from app.agent.errors import AgentError
from app.config import get_settings
from app.devices.service import acknowledge, issue_session, pending, register, rotate_session
from app.models import EventDelivery, OutboxEvent, RefreshFamily, RefreshToken, User
from app.security import decode_token


# Documentação: Implementa envelope como parte do fluxo descrito para este arquivo.
def envelope(kind, payload=None, identifier=None):
    return {"event_id": str(identifier or uuid4()), "type": kind, "payload": payload or {}}


# Documentação: Implementa authenticate como parte do fluxo descrito para este arquivo.
def authenticate(ws, user, device_id=None):
    from app.security import create_token

    identifier = device_id or uuid4()
    ws.send_json(
        envelope(
            "connection.authenticate",
            {"access_token": create_token(user, get_settings()), "device_id": str(identifier)},
        )
    )
    assert ws.receive_json()["type"] == "connection.ready"
    return identifier


# Documentação: Implementa receive como parte do fluxo descrito para este arquivo.
def receive(ws, kind):
    for _ in range(30):
        data = ws.receive_json()
        if data["type"] == "connection.ping":
            ws.send_json(envelope("connection.pong"))
        if data["type"] == "error" and kind != "error":
            pytest.fail("Unexpected WebSocket error: " + str(data["payload"]))
        if data["type"] == kind:
            return data
    pytest.fail("Expected frame not received")


# Documentação: Verifica o cenário test_refresh_rotation_reuse_invalidates_access; as condições e
# resultados esperados aparecem nos asserts.
def test_refresh_rotation_reuse_invalidates_access(client, session, user):
    device = str(uuid4())
    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": "test-password-only", "device_id": device},
    )
    assert response.status_code == 200
    first = response.json()
    assert decode_token(first["access_token"], get_settings())["sid"]
    assert session.get(RefreshToken, first["refresh_token"]) is None
    rotated = client.post("/auth/refresh", json={"refresh_token": first["refresh_token"]})
    assert rotated.status_code == 200
    assert rotated.json()["refresh_token"] != first["refresh_token"]
    assert (
        client.get(
            "/auth/me", headers={"Authorization": "Bearer " + rotated.json()["access_token"]}
        ).status_code
        == 200
    )
    assert (
        client.post("/auth/refresh", json={"refresh_token": first["refresh_token"]}).status_code
        == 401
    )
    assert (
        client.get(
            "/auth/me", headers={"Authorization": "Bearer " + rotated.json()["access_token"]}
        ).status_code
        == 401
    )
    session.expire_all()
    assert session.scalar(select(RefreshFamily)).revoked


# Documentação: Verifica o cenário test_device_revocation_and_other_owner_are_enforced; as
# condições e resultados esperados aparecem nos asserts.
def test_device_revocation_and_other_owner_are_enforced(client, session, user):
    device = uuid4()
    result = issue_session(session, user, device, get_settings())
    session.commit()
    other = User(username="other", password_hash=user.password_hash, timezone=user.timezone)
    session.add(other)
    session.commit()
    assert client.post(f"/devices/{device}/revoke", headers=headers(other)).status_code == 404
    assert client.get("/devices", headers=headers(other)).json() == []
    assert client.post(f"/devices/{device}/revoke", headers=headers(user)).status_code == 204
    assert (
        client.get(
            "/auth/me", headers={"Authorization": "Bearer " + result["access_token"]}
        ).status_code
        == 401
    )
    assert (
        client.post("/auth/refresh", json={"refresh_token": result["refresh_token"]}).status_code
        == 401
    )
    with pytest.raises(AgentError, match="device_unavailable"):
        register(session, device, user.id)


# Documentação: Verifica o cenário test_refresh_expiry_and_password_reset; as condições e
# resultados esperados aparecem nos asserts.
def test_refresh_expiry_and_password_reset(session, user):
    issued = issue_session(session, user, uuid4(), get_settings())
    session.commit()
    user.token_version += 1
    session.commit()
    with pytest.raises(AgentError, match="invalid_refresh"):
        rotate_session(session, issued["refresh_token"], get_settings())
    issued = issue_session(session, user, uuid4(), get_settings())
    session.commit()
    family = session.get(
        RefreshFamily, UUID(decode_token(issued["access_token"], get_settings())["sid"])
    )
    family.expires_at = datetime.now(UTC) - timedelta(seconds=1)
    session.commit()
    with pytest.raises(AgentError, match="invalid_refresh"):
        rotate_session(session, issued["refresh_token"], get_settings())


# Documentação: Verifica o cenário test_logout_revokes_device_session; as condições e resultados
# esperados aparecem nos asserts.
def test_logout_revokes_device_session(client, session, user):
    result = issue_session(session, user, uuid4(), get_settings())
    session.commit()
    auth = {"Authorization": "Bearer " + result["access_token"]}
    assert client.post("/auth/logout", headers=auth).status_code == 204
    assert client.get("/auth/me", headers=auth).status_code == 401


# Documentação: Verifica o cenário test_delivery_retries_and_ack_are_per_device; as condições e
# resultados esperados aparecem nos asserts.
def test_delivery_retries_and_ack_are_per_device(session, user):
    first, second = uuid4(), uuid4()
    register(session, first, user.id)
    register(session, second, user.id)
    event = OutboxEvent(
        user_id=user.id,
        type="reminder.triggered",
        payload={"text": "coffee"},
        dedupe_key="test-coffee",
    )
    session.add(event)
    session.commit()
    now = datetime.now(UTC)
    sent = pending(session, user.id, first, now)
    assert len(sent) == 1
    assert pending(session, user.id, first, now + timedelta(seconds=5)) == []
    assert pending(session, user.id, first, now + timedelta(seconds=16))[0]["event_id"] == str(
        event.id
    )
    acknowledge(session, user.id, first, event.id)
    acknowledge(session, user.id, first, event.id)
    assert pending(session, user.id, first, now + timedelta(seconds=32)) == []
    assert len(pending(session, user.id, second, now + timedelta(seconds=32))) == 1
    assert session.get(EventDelivery, (first, event.id)).attempts == 2
    assert event.status == "PENDING"


# Documentação: Verifica o cenário test_cancelled_and_foreign_events_cannot_be_acknowledged; as
# condições e resultados esperados aparecem nos asserts.
def test_cancelled_and_foreign_events_cannot_be_acknowledged(session, user):
    identifier = uuid4()
    register(session, identifier, user.id)
    session.add(
        OutboxEvent(
            user_id=user.id,
            type="reminder.triggered",
            payload={},
            dedupe_key="cancelled",
            status="CANCELLED",
        )
    )
    session.commit()
    assert pending(session, user.id, identifier) == []
    with pytest.raises(AgentError, match="event_not_found"):
        acknowledge(session, user.id, identifier, uuid4())
    with pytest.raises(AgentError, match="device_unavailable"):
        register(session, identifier, uuid4())


# Documentação: Verifica o cenário test_websocket_auth_heartbeat_and_validation; as condições e
# resultados esperados aparecem nos asserts.
def test_websocket_auth_heartbeat_and_validation(client, user):
    with client.websocket_connect("/ws") as ws:
        identifier = authenticate(ws, user)
        ws.send_json(envelope("connection.pong"))
        assert receive(ws, "connection.pong_ack")["payload"] == {}
        ws.send_json(envelope("HOST_SHELL", {"script": "secret-that-must-not-echo"}))
        assert receive(ws, "error")["payload"]["code"] == "event_type_not_available"
        ws.send_text('{"invalid":"secret-that-must-not-echo"}')
        assert "secret-that-must-not-echo" not in json.dumps(receive(ws, "error"))
    assert len(client.get("/devices", headers=headers(user)).json()) == 1
    assert str(identifier) == client.get("/devices", headers=headers(user)).json()[0]["id"]


# Documentação: Verifica o cenário test_websocket_invalid_auth_is_closed; as condições e
# resultados esperados aparecem nos asserts.
def test_websocket_invalid_auth_is_closed(client):
    with client.websocket_connect("/ws") as ws:
        ws.send_json(
            envelope(
                "connection.authenticate",
                {"access_token": "invalid-token" * 3, "device_id": str(uuid4())},
            )
        )
        with pytest.raises(WebSocketDisconnect) as issue:
            ws.receive_json()
        assert issue.value.code == 4401


# Documentação: Verifica o cenário test_websocket_chat_outbox_replay_no_second_inference; as
# condições e resultados esperados aparecem nos asserts.
def test_websocket_chat_outbox_replay_no_second_inference(client, session, user, monkeypatch):
    from contextlib import contextmanager

    import app.api.websocket as websocket_module
    from app.agent.core import AgentCore

    stub = StubRouter({"reply": "Olá pelo WebSocket", "actions": [], "memory_candidates": []})

    @contextmanager
    # Documentação: Implementa test_websocket_chat_outbox_replay_no_second_inference.factory como
    # parte do fluxo descrito para este arquivo.
    def factory(*_):
        yield stub

    monkeypatch.setattr(
        websocket_module,
        "AgentCore",
        lambda session, settings: AgentCore(session, settings, router_factory=factory),
    )
    identifier = uuid4()
    with client.websocket_connect("/ws") as ws:
        authenticate(ws, user)
        data = envelope(
            "chat.message", {"client_message_id": str(identifier), "content": "Olá"}, identifier
        )
        ws.send_json(data)
        response = receive(ws, "agent.message")
        assert response["payload"]["reply"] == "Olá pelo WebSocket"
        ws.send_json(envelope("event.ack", {"event_id": response["event_id"]}))
        receive(ws, "event.acknowledged")
        ws.send_json(data)
        while True:
            processed = receive(ws, "chat.processed")
            if processed["payload"]["replayed"]:
                break
        assert len(stub.calls) == 1
    assert (
        session.scalar(
            select(func.count()).select_from(OutboxEvent).where(OutboxEvent.type == "agent.message")
        )
        == 1
    )


# Documentação: Verifica o cenário
# test_websocket_device_bound_session_cannot_use_different_device; as condições e resultados
# esperados aparecem nos asserts.
def test_websocket_device_bound_session_cannot_use_different_device(client, session, user):
    result = issue_session(session, user, uuid4(), get_settings())
    session.commit()
    with client.websocket_connect("/ws") as ws:
        ws.send_json(
            envelope(
                "connection.authenticate",
                {"access_token": result["access_token"], "device_id": str(uuid4())},
            )
        )
        with pytest.raises(WebSocketDisconnect):
            ws.receive_json()
