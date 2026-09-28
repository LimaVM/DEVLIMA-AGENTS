import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_engine
from app.main import create_app
from app.models import (
    AgentAction,
    AuditLog,
    CallSession,
    Conversation,
    ConversationSummary,
    Device,
    EventDelivery,
    LLMRequest,
    LoginThrottle,
    Memory,
    MemoryCandidate,
    Message,
    OutboxEvent,
    RefreshFamily,
    RefreshToken,
    Schedule,
    ScheduledEvent,
    SchedulerHeartbeat,
    Task,
    User,
    Worker,
    WorkerCommand,
    WorkerSnapshot,
)
from app.security import hash_password


@pytest.fixture(autouse=True)
# Documentação: Implementa clean_test_database como parte do fluxo descrito para este arquivo.
def clean_test_database():
    settings = get_settings()
    if settings.postgres_db != "devlima_agent_test" or settings.postgres_host != "postgres-test":
        pytest.fail("Testes exigem o PostgreSQL efêmero postgres-test/devlima_agent_test")
    with Session(get_engine()) as session:
        for model in (
            CallSession,
            EventDelivery,
            RefreshToken,
            RefreshFamily,
            Device,
            WorkerSnapshot,
            WorkerCommand,
            Worker,
            OutboxEvent,
            ScheduledEvent,
            Schedule,
            SchedulerHeartbeat,
            Task,
            AgentAction,
            MemoryCandidate,
            Memory,
            ConversationSummary,
            Message,
            Conversation,
            LLMRequest,
            AuditLog,
            LoginThrottle,
            User,
        ):
            session.execute(delete(model))
        session.commit()
    yield


@pytest.fixture
# Documentação: Implementa session como parte do fluxo descrito para este arquivo.
def session():
    with Session(get_engine(), expire_on_commit=False) as db:
        yield db


@pytest.fixture
# Documentação: Implementa user como parte do fluxo descrito para este arquivo.
def user(session):
    user = User(
        username="testuser",
        password_hash=hash_password("test-password-only"),
        timezone="America/Sao_Paulo",
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
# Documentação: Implementa client como parte do fluxo descrito para este arquivo.
def client():
    with TestClient(create_app()) as client:
        yield client
