"""Audited LLM attempts without prompts, replies or credentials."""

import sqlalchemy as sa
from alembic import op

revision = "0002_llm_requests"
down_revision = "0001_identity"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "llm_requests",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("request_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("model", sa.String(512), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("fallback", sa.Boolean(), nullable=False),
        sa.Column("error_code", sa.String(64)),
        sa.Column("status_code", sa.Integer()),
        sa.Column("upstream_request_id", sa.String(255)),
        sa.Column("prompt_tokens", sa.Integer()),
        sa.Column("completion_tokens", sa.Integer()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    for name in ("request_id", "user_id", "created_at"):
        op.create_index(f"ix_llm_requests_{name}", "llm_requests", [name])


def downgrade() -> None:
    op.drop_table("llm_requests")
