"""Persistent conversations, bounded summaries, memories and validated actions."""

import sqlalchemy as sa
from alembic import op

revision = "0003_context"
down_revision = "0002_llm_requests"
branch_labels = None
depends_on = None


# Documentação: Implementa identifier como parte do fluxo descrito para este arquivo.
def identifier():
    return sa.Column("id", sa.Uuid(), primary_key=True)


# Documentação: Implementa owner como parte do fluxo descrito para este arquivo.
def owner():
    return sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False)


# Documentação: Implementa timestamp como parte do fluxo descrito para este arquivo.
def timestamp(name="created_at"):
    return sa.Column(name, sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)


# Documentação: Aplica tabelas, campos, índices e constraints desta revisão Alembic.
def upgrade():
    op.create_table(
        "conversations",
        identifier(),
        owner(),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("archived", sa.Boolean(), nullable=False),
        sa.Column("last_sequence", sa.Integer(), nullable=False),
        sa.Column("lease_owner", sa.Uuid()),
        sa.Column("lease_until", sa.DateTime(timezone=True)),
        sa.Column("pending_message_id", sa.Uuid()),
        timestamp(),
        timestamp("updated_at"),
    )
    op.create_table(
        "messages",
        identifier(),
        owner(),
        sa.Column("conversation_id", sa.Uuid(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("client_message_id", sa.Uuid()),
        sa.Column("in_reply_to", sa.Uuid(), sa.ForeignKey("messages.id")),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("error_code", sa.String(64)),
        sa.Column("info", sa.JSON(), nullable=False),
        timestamp(),
        sa.UniqueConstraint("conversation_id", "sequence", name="uq_messages_sequence"),
        sa.UniqueConstraint("user_id", "client_message_id", name="uq_messages_client_id"),
        sa.UniqueConstraint("in_reply_to", name="uq_messages_reply"),
        sa.CheckConstraint("role IN ('user', 'assistant')", name="ck_messages_role"),
    )
    op.create_table(
        "conversation_summaries",
        identifier(),
        owner(),
        sa.Column("conversation_id", sa.Uuid(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("through_sequence", sa.Integer(), nullable=False),
        sa.Column("content", sa.JSON(), nullable=False),
        timestamp(),
        sa.UniqueConstraint("conversation_id", "through_sequence", name="uq_summary_coverage"),
    )
    op.create_table(
        "memories",
        identifier(),
        owner(),
        sa.Column("source_message_id", sa.Uuid(), sa.ForeignKey("messages.id")),
        sa.Column("content", sa.String(1000), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        timestamp(),
        timestamp("updated_at"),
        sa.UniqueConstraint("user_id", "content_hash", name="uq_memories_content"),
    )
    op.create_table(
        "memory_candidates",
        identifier(),
        owner(),
        sa.Column("source_message_id", sa.Uuid(), sa.ForeignKey("messages.id"), nullable=False),
        sa.Column("accepted_memory_id", sa.Uuid(), sa.ForeignKey("memories.id")),
        sa.Column("content", sa.String(1000), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("rejection_reason", sa.String(64)),
        timestamp(),
        sa.UniqueConstraint("source_message_id", "content_hash", name="uq_candidate_source"),
    )
    op.create_table(
        "agent_actions",
        identifier(),
        owner(),
        sa.Column("source_message_id", sa.Uuid(), sa.ForeignKey("messages.id"), nullable=False),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("arguments", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        timestamp(),
    )
    for table, columns in {
        "conversations": ("user_id", "updated_at"),
        "messages": ("user_id", "conversation_id"),
        "conversation_summaries": ("user_id", "conversation_id"),
        "memories": ("user_id",),
        "memory_candidates": ("user_id",),
        "agent_actions": ("user_id",),
    }.items():
        for column in columns:
            op.create_index(f"ix_{table}_{column}", table, [column])


# Documentação: Reverte os elementos de schema criados por esta revisão, respeitando dependências.
def downgrade():
    for table in (
        "agent_actions",
        "memory_candidates",
        "memories",
        "conversation_summaries",
        "messages",
        "conversations",
    ):
        op.drop_table(table)
