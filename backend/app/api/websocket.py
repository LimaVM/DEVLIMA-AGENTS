import asyncio
import contextlib
import json
import logging
import time
from datetime import UTC, datetime
from uuid import UUID, uuid4

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.agent.action_parser import reject_duplicate_keys
from app.agent.core import AgentCore
from app.agent.errors import AgentError
from app.config import get_settings
from app.db.session import get_engine
from app.devices.service import acknowledge, authorize_claims, pending, register
from app.llm.base import LLMError
from app.models.devices import Device, RefreshFamily
from app.schemas.chat import ChatSend
from app.security import decode_token

router = APIRouter()
logger = logging.getLogger("devlima.websocket")


class Envelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: UUID
    timestamp: str | None = Field(None, max_length=64)
    type: str = Field(min_length=1, max_length=64)
    payload: dict = Field(default_factory=dict)


class Authenticate(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)
    access_token: str = Field(min_length=20, max_length=4096)
    device_id: UUID
    name: str = Field("Android", min_length=1, max_length=64)


class Ack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: UUID


def authenticate(data, connection_id):
    settings = get_settings()
    claims = decode_token(data.access_token, settings)
    with Session(get_engine(), expire_on_commit=False) as session:
        user = authorize_claims(session, claims)
        if "sid" in claims:
            family = session.get(RefreshFamily, UUID(claims["sid"]))
            if family.device_id != data.device_id:
                raise AgentError("device_session_mismatch", 403)
        device = register(session, data.device_id, user.id, data.name)
        device.connection_id = connection_id
        session.commit()
        return user.id


def verify(token, owner, device_id, connection_id):
    claims = decode_token(token, get_settings())
    with Session(get_engine(), expire_on_commit=False) as session:
        user = authorize_claims(session, claims)
        device = session.get(Device, device_id)
        if (
            user.id != owner
            or device is None
            or device.user_id != owner
            or device.revoked
            or device.connection_id != connection_id
        ):
            raise AgentError("device_connection_replaced", 403)
        return True


def events(owner, device_id):
    with Session(get_engine(), expire_on_commit=False) as session:
        return pending(session, owner, device_id)


def ack_event(owner, device_id, event_id):
    with Session(get_engine()) as session:
        acknowledge(session, owner, device_id, event_id)


def chat(owner, data):
    with Session(get_engine(), expire_on_commit=False) as session:
        return AgentCore(session, get_settings()).send(owner, data)


@router.websocket("/ws")
async def websocket(socket: WebSocket):
    if socket.query_params:
        await socket.close(code=1008)
        return
    await socket.accept()
    connection_id, device_id, owner = uuid4(), None, None
    jobs, writer, stopped = set(), asyncio.Lock(), asyncio.Event()
    last_pong, token = time.monotonic(), ""

    async def send(kind, payload, event_id=None):
        async with writer:
            if not stopped.is_set():
                await socket.send_json(
                    {
                        "event_id": str(event_id or uuid4()),
                        "timestamp": datetime.now(UTC).isoformat(),
                        "type": kind,
                        "payload": payload,
                    }
                )

    async def transmit(raw):
        async with writer:
            if not stopped.is_set():
                await socket.send_json(raw)

    async def process_chat(data, request_id):
        try:
            # The Core writes agent.message to its durable outbox in the same transaction.
            reply = await run_in_threadpool(chat, owner, data)
            await send(
                "chat.processed",
                {
                    "client_message_id": str(data.client_message_id),
                    "assistant_message_id": str(reply.assistant_message_id),
                    "replayed": reply.replayed,
                },
                request_id,
            )
        except (AgentError, LLMError) as error:
            await send(
                "error",
                {"code": error.code, "client_message_id": str(data.client_message_id)},
                request_id,
            )
        except Exception:
            logger.error("websocket_chat_failed")
            with contextlib.suppress(RuntimeError, WebSocketDisconnect):
                await send(
                    "error",
                    {
                        "code": "service_unavailable",
                        "client_message_id": str(data.client_message_id),
                    },
                    request_id,
                )

    async def pump():
        ping_at = time.monotonic()
        try:
            while not stopped.is_set():
                await run_in_threadpool(verify, token, owner, device_id, connection_id)
                if time.monotonic() - last_pong > 60:
                    await socket.close(4408)
                    return
                for event in await run_in_threadpool(events, owner, device_id):
                    await transmit(event)
                if time.monotonic() >= ping_at:
                    await send("connection.ping", {})
                    ping_at = time.monotonic() + 20
                await asyncio.sleep(1)
        except (jwt.InvalidTokenError, ValueError, AgentError):
            with contextlib.suppress(RuntimeError, WebSocketDisconnect):
                await send("error", {"code": "authentication_expired_or_revoked"})
                await socket.close(4401)
        except (RuntimeError, WebSocketDisconnect):
            pass
        except Exception:
            logger.error("websocket_delivery_failed")
            with contextlib.suppress(RuntimeError, WebSocketDisconnect):
                await socket.close(1011)
        finally:
            stopped.set()

    pump_task = None
    try:
        raw = await asyncio.wait_for(socket.receive_text(), timeout=10)
        if len(raw) > 16384:
            raise ValueError("frame_too_large")
        first = Envelope.model_validate(json.loads(raw, object_pairs_hook=reject_duplicate_keys))
        if first.type != "connection.authenticate":
            raise ValueError("authentication_required")
        credentials = Authenticate.model_validate(first.payload)
        token, device_id = credentials.access_token, credentials.device_id
        owner = await run_in_threadpool(authenticate, credentials, connection_id)
        await send(
            "connection.ready",
            {"device_id": str(device_id), "heartbeat_seconds": 20, "protocol": 1},
        )
        pump_task = asyncio.create_task(pump())
        while not stopped.is_set():
            raw = await socket.receive_text()
            if len(raw) > 16384:
                await socket.close(1009)
                break
            try:
                envelope = Envelope.model_validate(
                    json.loads(raw, object_pairs_hook=reject_duplicate_keys)
                )
                await run_in_threadpool(verify, token, owner, device_id, connection_id)
                if envelope.type == "connection.pong":
                    if envelope.payload:
                        raise ValueError("invalid_pong")
                    last_pong = time.monotonic()
                    await send("connection.pong_ack", {}, envelope.event_id)
                elif envelope.type == "event.ack":
                    await run_in_threadpool(
                        ack_event, owner, device_id, Ack.model_validate(envelope.payload).event_id
                    )
                    await send(
                        "event.acknowledged",
                        {"event_id": envelope.payload["event_id"]},
                        envelope.event_id,
                    )
                elif envelope.type == "chat.message":
                    data = ChatSend.model_validate(envelope.payload)
                    if envelope.event_id != data.client_message_id:
                        raise ValueError("message_id_mismatch")
                    if len(jobs) >= 1:
                        await send(
                            "error",
                            {
                                "code": "device_busy",
                                "client_message_id": str(data.client_message_id),
                            },
                            envelope.event_id,
                        )
                    else:
                        task = asyncio.create_task(process_chat(data, envelope.event_id))
                        jobs.add(task)
                        task.add_done_callback(jobs.discard)
                        await send(
                            "chat.accepted",
                            {"client_message_id": str(data.client_message_id)},
                            envelope.event_id,
                        )
                else:
                    await send("error", {"code": "event_type_not_available"}, envelope.event_id)
            except (ValidationError, ValueError, TypeError, KeyError, RecursionError):
                await send("error", {"code": "invalid_event"})
            except AgentError as error:
                await send("error", {"code": error.code})
            except jwt.InvalidTokenError:
                await socket.close(4401)
                break
    except (
        jwt.InvalidTokenError,
        AgentError,
        ValidationError,
        ValueError,
        TypeError,
        KeyError,
        TimeoutError,
        RecursionError,
    ):
        with contextlib.suppress(RuntimeError, WebSocketDisconnect):
            await socket.close(4401)
    except (WebSocketDisconnect, RuntimeError):
        pass
    finally:
        stopped.set()
        if pump_task:
            pump_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await pump_task
        # Core work already running in a thread may finish safely into PostgreSQL/outbox.
        for task in list(jobs):
            task.cancel()
        if jobs:
            await asyncio.gather(*jobs, return_exceptions=True)
