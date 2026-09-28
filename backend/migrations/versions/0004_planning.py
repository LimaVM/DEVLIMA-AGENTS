"""Durable tasks, schedules, occurrences, outbox and scheduler heartbeat."""

import sqlalchemy as sa
from alembic import op

revision = "0004_planning"
down_revision = "0003_context"
branch_labels = None
depends_on = None


def identifier():
    return sa.Column("id", sa.Uuid(), primary_key=True)


def owner():
    return sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False)


def timestamp(name="created_at"):
    return sa.Column(name, sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())


def upgrade():
    op.create_table(
        "tasks",
        identifier(),
        owner(),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("due_at", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(16), nullable=False),
        timestamp(),
        timestamp("updated_at"),
    )
    op.create_table(
        "schedules",
        identifier(),
        owner(),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("text", sa.String(1000), nullable=False),
        sa.Column("timezone", sa.String(80), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("next_run_at", sa.DateTime(timezone=True)),
        sa.Column("rrule", sa.String(500)),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        timestamp(),
        timestamp("updated_at"),
    )
    op.create_table(
        "scheduled_events",
        identifier(),
        owner(),
        sa.Column("schedule_id", sa.Uuid(), sa.ForeignKey("schedules.id"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        timestamp("executed_at"),
        sa.Column("status", sa.String(16), nullable=False),
        sa.UniqueConstraint(
            "schedule_id", "version", "scheduled_at", name="uq_schedule_occurrence"
        ),
    )
    op.create_table(
        "outbox_events",
        identifier(),
        owner(),
        sa.Column("schedule_id", sa.Uuid(), sa.ForeignKey("schedules.id")),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("dedupe_key", sa.String(160), nullable=False, unique=True),
        sa.Column("status", sa.String(16), nullable=False),
        timestamp(),
    )
    op.create_table(
        "scheduler_heartbeats",
        sa.Column("name", sa.String(40), primary_key=True),
        sa.Column("last_tick_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("processed", sa.Integer(), nullable=False),
    )
    for table, columns in {
        "tasks": ("user_id", "due_at"),
        "schedules": ("user_id", "kind", "next_run_at", "status"),
        "scheduled_events": ("user_id", "schedule_id"),
        "outbox_events": ("user_id", "schedule_id", "status", "created_at"),
    }.items():
        for column in columns:
            op.create_index(f"ix_{table}_{column}", table, [column])


def downgrade():
    for table in (
        "scheduler_heartbeats",
        "outbox_events",
        "scheduled_events",
        "schedules",
        "tasks",
    ):
        op.drop_table(table)
