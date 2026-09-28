import hashlib
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, ConfigDict, Field, SecretStr
from sqlalchemy import case, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.agent.errors import AgentError
from app.config import Settings, get_settings
from app.db.session import get_session
from app.devices.service import issue_session, logout, rotate_session
from app.models import AuditLog, LoginThrottle, User
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.security import (
    bearer,
    create_token,
    decode_token,
    dummy_hash,
    get_current_user,
    password_hasher,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# Documentação: Implementa consume_login_attempt como parte do fluxo descrito para este arquivo.
def consume_login_attempt(session: Session, bucket: str, settings: Settings) -> None:
    now = datetime.now(UTC)
    expired = LoginThrottle.window_started_at <= now - timedelta(
        seconds=settings.login_window_seconds
    )
    statement = insert(LoginThrottle).values(bucket=bucket, attempts=1, window_started_at=now)
    statement = statement.on_conflict_do_update(
        index_elements=[LoginThrottle.bucket],
        set_={
            "attempts": case((expired, 1), else_=LoginThrottle.attempts + 1),
            "window_started_at": case((expired, now), else_=LoginThrottle.window_started_at),
        },
    ).returning(LoginThrottle.attempts)
    attempts = session.execute(statement).scalar_one()
    # Commit before HTTPException: the limit must survive failures/restarts.
    session.commit()
    if attempts > settings.login_max_attempts:
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas de login; tente novamente mais tarde",
            headers={"Retry-After": str(settings.login_window_seconds)},
        )


@router.post("/login", response_model=TokenResponse)
# Documentação: Implementa login como parte do fluxo descrito para este arquivo.
def login(
    data: LoginRequest,
    request: Request,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    ip = request.client.host if request.client else "unknown"
    bucket = hashlib.sha256(ip.encode()).hexdigest()
    consume_login_attempt(session, bucket, settings)
    user = session.scalar(select(User).where(User.username == data.username.lower()))
    valid = verify_password(
        user.password_hash if user else dummy_hash, data.password.get_secret_value()
    )
    if not valid or user is None or not user.is_active:
        session.add(
            AuditLog(
                event="auth.login_failed",
                request_id=request.state.request_id,
                details={"ip_hash": bucket},
            )
        )
        session.commit()
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    if password_hasher.check_needs_rehash(user.password_hash):
        user.password_hash = password_hasher.hash(data.password.get_secret_value())
    session.add(
        AuditLog(
            user_id=user.id,
            event="auth.login_success",
            request_id=request.state.request_id,
            details={"ip_hash": bucket},
        )
    )
    if data.device_id is not None:
        try:
            result = issue_session(session, user, data.device_id, settings)
        except AgentError as error:
            session.rollback()
            raise HTTPException(error.status_code, error.code) from None
        session.commit()
        return TokenResponse(**result)
    session.commit()
    return TokenResponse(
        access_token=create_token(user, settings), expires_in=settings.jwt_ttl_minutes * 60
    )


@router.get("/me", response_model=UserResponse)
# Documentação: Implementa me como parte do fluxo descrito para este arquivo.
def me(user: User = Depends(get_current_user)) -> User:
    return user


# Documentação: Define o tipo RefreshRequest e reúne o estado/contrato descrito para este módulo.
class RefreshRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)
    refresh_token: SecretStr = Field(min_length=32, max_length=128)


@router.post("/refresh", response_model=TokenResponse)
# Documentação: Atualiza refresh, segundo o contrato e as verificações deste módulo.
def refresh(
    data: RefreshRequest,
    request: Request,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    bucket = hashlib.sha256(
        (request.client.host if request.client else "unknown").encode()
    ).hexdigest()
    consume_login_attempt(session, bucket, settings)
    try:
        result = rotate_session(session, data.refresh_token.get_secret_value(), settings)
        session.commit()
        return TokenResponse(**result)
    except AgentError as error:
        session.rollback()
        raise HTTPException(error.status_code, error.code) from None


@router.post("/logout", status_code=204)
# Documentação: Implementa sign_out como parte do fluxo descrito para este arquivo.
def sign_out(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    claims = decode_token(credentials.credentials, settings)
    if "sid" not in claims:
        user.token_version += 1
    logout(session, claims)
