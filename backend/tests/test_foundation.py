from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app import cli
from app.api.auth import consume_login_attempt
from app.config import Settings, get_settings
from app.db.session import get_engine
from app.models import AuditLog, LoginThrottle, User
from app.security import create_token, decode_token, hash_password, verify_password


def test_health_and_request_id(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["schema"] == "0005_workers"
    assert UUID(response.headers["X-Request-ID"])
    assert response.headers["Cache-Control"] == "no-store"
    assert client.get("/health/live").json()["status"] == "ok"


def test_docs_disabled(client):
    assert client.get("/docs").status_code == 404
    assert client.get("/openapi.json").status_code == 404


def test_database_error_does_not_expose_secrets(client, monkeypatch):
    def fail():
        raise OperationalError("secret-query", {"password": "sensitive"}, Exception("secret"))

    monkeypatch.setattr("app.main.get_engine", fail)
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert "secret" not in response.text
    assert "sensitive" not in response.text


@pytest.mark.parametrize("name,value", [("jwt_secret", "short"), ("postgres_password", "short")])
def test_short_secrets_refused(name, value):
    with pytest.raises(ValidationError):
        Settings(**{name: value})


def test_invalid_timezone_refused():
    with pytest.raises(ValidationError):
        Settings(default_timezone="not/a/timezone")


def test_password_hash_and_wrong_password():
    hashed = hash_password("test-password-only")
    assert hashed.startswith("$argon2id$")
    assert verify_password(hashed, "test-password-only")
    assert not verify_password(hashed, "incorrect")
    assert not verify_password("not-a-hash", "incorrect")


@pytest.mark.parametrize("password", ["short", "a" * 1025])
def test_password_length_policy(password):
    with pytest.raises(ValueError):
        hash_password(password)


def test_authentication_and_audit(client, user, session):
    response = client.post(
        "/auth/login", json={"username": "TESTUSER", "password": "test-password-only"}
    )
    assert response.status_code == 200
    assert response.json()["expires_in"] == 1800
    token = response.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["id"] == str(user.id)
    assert me.json()["timezone"] == "America/Sao_Paulo"
    assert "password" not in me.text
    audit = session.scalar(select(AuditLog).where(AuditLog.event == "auth.login_success"))
    assert audit.user_id == user.id
    assert audit.request_id == response.headers["X-Request-ID"]
    assert "password" not in str(audit.details)


@pytest.mark.parametrize("username", ["testuser", "unknown"])
def test_invalid_login_indistinguishable(client, user, username):
    response = client.post("/auth/login", json={"username": username, "password": "incorrect"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Usuário ou senha inválidos"}


def test_missing_or_invalid_auth(client):
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer invalid"}).status_code == 401


def test_validation_does_not_echo_password(client):
    secret = "sensitive-input-must-not-be-echoed"
    response = client.post("/auth/login", json={"username": "invalid name", "password": secret})
    assert response.status_code == 422
    assert secret not in response.text
    assert "input" not in response.json()["detail"][0]
    extra = client.post(
        "/auth/login", json={"username": "user", "password": "valid", "token": secret}
    )
    assert extra.status_code == 422
    assert secret not in extra.text


def test_token_signature_audience_and_expiration(user):
    settings = get_settings()
    token = create_token(user, settings)
    claims = decode_token(token, settings)
    assert claims["sub"] == str(user.id)
    for mutation in ({"aud": "wrong"}, {"exp": datetime.now(UTC) - timedelta(seconds=1)}):
        bad = jwt.encode(
            claims | mutation, settings.jwt_secret.get_secret_value(), algorithm="HS256"
        )
        with pytest.raises(jwt.InvalidTokenError):
            decode_token(bad, settings)
    forged = jwt.encode(claims, "wrong-secret-that-is-long-enough-1234", algorithm="HS256")
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(forged, settings)


def test_reset_password_revokes_existing_tokens(client, user, session):
    token = create_token(user, get_settings())
    user.token_version += 1
    session.commit()
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_inactive_user_cannot_login_or_use_token(client, user, session):
    token = create_token(user, get_settings())
    user.is_active = False
    session.commit()
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    assert (
        client.post(
            "/auth/login", json={"username": "testuser", "password": "test-password-only"}
        ).status_code
        == 401
    )


def test_login_limit_persists_across_sessions(client, session):
    for _ in range(5):
        assert (
            client.post(
                "/auth/login", json={"username": "unknown", "password": "wrong"}
            ).status_code
            == 401
        )
    response = client.post("/auth/login", json={"username": "unknown", "password": "wrong"})
    assert response.status_code == 429
    assert response.headers["Retry-After"] == "900"
    with Session(get_engine()) as independent:
        assert independent.scalar(select(LoginThrottle.attempts)) == 6
    assert session.scalar(select(func.count()).select_from(AuditLog)) == 5


def test_login_limit_atomic_under_concurrency():
    bucket = str(uuid4())

    def attempt(_):
        with Session(get_engine()) as db:
            try:
                consume_login_attempt(db, bucket, get_settings())
                return 200
            except HTTPException as error:
                return error.status_code

    with ThreadPoolExecutor(max_workers=10) as pool:
        statuses = list(pool.map(attempt, range(10)))
    assert statuses.count(200) == 5
    assert statuses.count(429) == 5
    with Session(get_engine()) as db:
        assert db.get(LoginThrottle, bucket).attempts == 10


def test_expired_login_window_resets(session):
    bucket = "old-window"
    session.add(
        LoginThrottle(
            bucket=bucket, attempts=99, window_started_at=datetime.now(UTC) - timedelta(hours=1)
        )
    )
    session.commit()
    consume_login_attempt(session, bucket, get_settings())
    session.expire_all()
    assert session.get(LoginThrottle, bucket).attempts == 1


def test_cli_create_list_reset(monkeypatch, capsys, session):
    monkeypatch.setattr("sys.argv", ["cli", "create-user", "owner"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: "test-password-only")
    cli.main()
    user = session.scalar(select(User).where(User.username == "owner"))
    assert user is not None
    assert user.token_version == 0
    monkeypatch.setattr("sys.argv", ["cli", "list-users"])
    cli.main()
    assert "owner" in capsys.readouterr().out
    monkeypatch.setattr("sys.argv", ["cli", "reset-password", "owner"])
    cli.main()
    session.refresh(user)
    assert user.token_version == 1
    assert session.scalar(select(func.count()).select_from(AuditLog)) == 2
