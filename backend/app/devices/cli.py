"""Real Uvicorn/WebSocket protocol smoke in the isolated database, plus public TLS probe."""

import json
import threading
import time
from uuid import uuid4

import uvicorn
from sqlalchemy.orm import Session
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect

from app.config import get_settings
from app.db.session import get_engine
from app.main import create_app
from app.models import OutboxEvent, User
from app.security import create_token, hash_password


# Documentação: Implementa frame como parte do fluxo descrito para este arquivo.
def frame(kind, payload=None):
    return json.dumps({"event_id": str(uuid4()), "type": kind, "payload": payload or {}})


# Documentação: Implementa receive como parte do fluxo descrito para este arquivo.
def receive(socket, kind):
    for _ in range(20):
        event = json.loads(socket.recv(timeout=5))
        if event["type"] == "connection.ping":
            socket.send(frame("connection.pong"))
        if event["type"] == kind:
            return event
    raise RuntimeError("Expected frame unavailable")


# Documentação: Coordena a entrada de linha de comando deste arquivo: Executa smoke WSS com
# dispositivo e usuário sintéticos, frames reais, reconexão e ACK, sem embutir credenciais
# operacionais.
def main():
    settings = get_settings()
    if settings.postgres_host != "postgres-test" or settings.postgres_db != "devlima_agent_test":
        raise SystemExit("Smoke requires isolated database")
    with Session(get_engine(), expire_on_commit=False) as session:
        user = User(
            username="ws-smoke-" + uuid4().hex[:12],
            password_hash=hash_password(uuid4().hex),
            timezone="America/Sao_Paulo",
        )
        session.add(user)
        session.flush()
        event = OutboxEvent(
            user_id=user.id,
            type="reminder.triggered",
            payload={"text": "protocol smoke"},
            dedupe_key="ws-smoke:" + str(uuid4()),
        )
        session.add(event)
        session.commit()
        event_id, token = str(event.id), create_token(user, settings)
    server = uvicorn.Server(
        uvicorn.Config(
            create_app(),
            host="127.0.0.1",
            port=8765,
            ws="websockets-sansio",
            ws_max_size=16384,
            access_log=False,
            log_level="warning",
        )
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 15
    while not server.started:
        if time.monotonic() > deadline:
            raise RuntimeError("Test server unavailable")
        time.sleep(0.1)
    device = str(uuid4())
    try:
        with connect("ws://127.0.0.1:8765/ws", open_timeout=5) as socket:
            socket.send(
                frame("connection.authenticate", {"access_token": token, "device_id": device})
            )
            assert receive(socket, "connection.ready")["payload"]["protocol"] == 1
            reminder = receive(socket, "reminder.triggered")
            assert reminder["event_id"] == event_id
            socket.send(frame("event.ack", {"event_id": event_id}))
            assert receive(socket, "event.acknowledged")["payload"]["event_id"] == event_id
            socket.send(frame("connection.pong"))
            receive(socket, "connection.pong_ack")
        with connect("ws://127.0.0.1:8765/ws", open_timeout=5) as socket:
            socket.send(
                frame("connection.authenticate", {"access_token": token, "device_id": device})
            )
            receive(socket, "connection.ready")
            socket.send(frame("connection.pong"))
            receive(socket, "connection.pong_ack")
            # Persistent ACK is checked through the DB, not a process-local cache.
            from app.models.devices import EventDelivery

            with Session(get_engine()) as session:
                from uuid import UUID

                assert (
                    session.get(EventDelivery, (UUID(device), UUID(event_id))).acknowledged_at
                    is not None
                )
        with connect("wss://agent.vegasolucoes.com.br/ws", open_timeout=10) as socket:
            socket.send(
                frame(
                    "connection.authenticate",
                    {
                        "access_token": "invalid-probe-token-that-is-not-a-credential",
                        "device_id": str(uuid4()),
                    },
                )
            )
            try:
                socket.recv(timeout=5)
                raise AssertionError("Invalid token accepted")
            except ConnectionClosed as error:
                assert error.rcvd is not None and error.rcvd.code == 4401
        print(
            json.dumps(
                {
                    "result": "passed",
                    "transport": "Uvicorn/websockets-sansio",
                    "authenticated_delivery": True,
                    "persistent_ack": True,
                    "public_wss_tls": True,
                    "invalid_token_rejected": True,
                }
            )
        )
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        if thread.is_alive():
            raise RuntimeError("Test server did not stop")


if __name__ == "__main__":
    main()
