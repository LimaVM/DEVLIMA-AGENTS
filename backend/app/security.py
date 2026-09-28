from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db.session import get_session
from app.models import User

password_hasher = PasswordHasher()
dummy_hash = password_hasher.hash("dummy-password-for-timing-only")
bearer = HTTPBearer(auto_error=False)


# Documentação: Produz hash Argon2 da senha; o valor original não deve ser persistido.
def hash_password(password: str) -> str:
    if not 12 <= len(password) <= 1024:
        raise ValueError("Senha deve ter entre 12 e 1024 caracteres")
    return password_hasher.hash(password)


# Documentação: Confere a senha fornecida contra seu hash e trata hash inválido como rejeição.
def verify_password(password_hash: str, password: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError):
        return False


# Documentação: Emite JWT com claims, validade, issuer/audience e versão de revogação definidos
# pelo serviço.
def create_token(user: User, settings: Settings, session_id=None) -> str:
    now = datetime.now(UTC)
    return jwt.encode(
        {
            "sub": str(user.id),
            "ver": user.token_version,
            "iat": now,
            "exp": now + timedelta(minutes=settings.jwt_ttl_minutes),
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "jti": str(uuid4()),
            **({"sid": str(session_id)} if session_id is not None else {}),
        },
        settings.jwt_secret.get_secret_value(),
        algorithm="HS256",
    )


# Documentação: Verifica assinatura e claims obrigatórios antes de aceitar a identidade do JWT.
def decode_token(token: str, settings: Settings) -> dict:
    claims = jwt.decode(
        token,
        settings.jwt_secret.get_secret_value(),
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
        options={"require": ["sub", "ver", "iat", "exp", "iss", "aud", "jti"]},
    )
    UUID(claims["sub"])
    if type(claims["ver"]) is not int:
        raise ValueError("Versão inválida")
    return claims


# Documentação: Valida JWT e estado do usuário no banco antes de disponibilizar identidade à rota.
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> User:
    error = HTTPException(
        status_code=401,
        detail="Autenticação inválida ou expirada",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise error
    try:
        claims = decode_token(credentials.credentials, settings)
        from app.devices.service import authorize_claims

        user = authorize_claims(session, claims)
    except (jwt.InvalidTokenError, ValueError, TypeError, KeyError):
        raise error from None
    return user
