"""Devices, rotating refresh sessions and per-device delivery acknowledgments."""

import sqlalchemy as sa
from alembic import op

revision = "0006_devices"
down_revision = "0005_workers"
branch_labels = None
depends_on = None


# Documentação: Implementa owner como parte do fluxo descrito para este arquivo.
def owner():
    return sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False)


# Documentação: Implementa created como parte do fluxo descrito para este arquivo.
def created():
    return sa.Column(
        "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )


# Documentação: Aplica tabelas, campos, índices e constraints desta revisão Alembic.
def upgrade():
    op.create_table(
        "devices",
        sa.Column("id", sa.Uuid(), primary_key=True),
        owner(),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("connection_id", sa.Uuid()),
        sa.Column(
            "last_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        created(),
    )
    op.create_table(
        "refresh_families",
        sa.Column("id", sa.Uuid(), primary_key=True),
        owner(),
        sa.Column("device_id", sa.Uuid(), sa.ForeignKey("devices.id"), nullable=False),
        sa.Column("token_version", sa.Integer(), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        created(),
    )
    op.create_table(
        "refresh_tokens",
        sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column("family_id", sa.Uuid(), sa.ForeignKey("refresh_families.id"), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False),
        created(),
    )
    op.create_table(
        "event_deliveries",
        sa.Column("device_id", sa.Uuid(), sa.ForeignKey("devices.id"), primary_key=True),
        sa.Column("event_id", sa.Uuid(), sa.ForeignKey("outbox_events.id"), primary_key=True),
        owner(),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True)),
        sa.Column("attempts", sa.Integer(), nullable=False),
    )
    for table, columns in {
        "devices": ["user_id"],
        "refresh_families": ["user_id", "device_id"],
        "refresh_tokens": ["family_id"],
        "event_deliveries": ["user_id"],
    }.items():
        for column in columns:
            op.create_index(f"ix_{table}_{column}", table, [column])


# Documentação: Reverte os elementos de schema criados por esta revisão, respeitando dependências.
def downgrade():
    for table in ["event_deliveries", "refresh_tokens", "refresh_families", "devices"]:
        op.drop_table(table)
