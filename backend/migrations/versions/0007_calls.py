"""Internal call sessions; one session per incoming occurrence."""

import sqlalchemy as sa
from alembic import op

revision = "0007_calls"
down_revision = "0006_devices"
branch_labels = None
depends_on = None


# Documentação: Aplica tabelas, campos, índices e constraints desta revisão Alembic.
def upgrade():
    op.create_table(
        "call_sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("device_id", sa.Uuid(), sa.ForeignKey("devices.id"), nullable=False),
        sa.Column(
            "incoming_event_id",
            sa.Uuid(),
            sa.ForeignKey("outbox_events.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("conversation_id", sa.Uuid(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("reason", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column(
            "started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "last_active_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
    )
    for column in ("user_id", "device_id", "conversation_id", "status"):
        op.create_index(f"ix_call_sessions_{column}", "call_sessions", [column])


# Documentação: Reverte os elementos de schema criados por esta revisão, respeitando dependências.
def downgrade():
    op.drop_table("call_sessions")
