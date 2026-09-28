from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


# Documentação: Define o tipo Device e reúne o estado/contrato descrito para este módulo.
class Device(Base):
    __tablename__ = "devices"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(64), default="Android")
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    connection_id: Mapped[UUID | None] = mapped_column()
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Documentação: Define o tipo RefreshFamily e reúne o estado/contrato descrito para este módulo.
class RefreshFamily(Base):
    __tablename__ = "refresh_families"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    device_id: Mapped[UUID] = mapped_column(ForeignKey("devices.id"), index=True)
    token_version: Mapped[int] = mapped_column(Integer)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Documentação: Define o tipo RefreshToken e reúne o estado/contrato descrito para este módulo.
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    family_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_families.id"), index=True)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Documentação: Define o tipo EventDelivery e reúne o estado/contrato descrito para este módulo.
class EventDelivery(Base):
    __tablename__ = "event_deliveries"
    device_id: Mapped[UUID] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("outbox_events.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    attempts: Mapped[int] = mapped_column(Integer, default=1)
