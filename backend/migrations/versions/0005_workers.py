"""Workers and durable host-operation queue."""

import sqlalchemy as sa
from alembic import op

revision = "0005_workers"
down_revision = "0004_planning"
branch_labels = None
depends_on = None


def identifier():
    return sa.Column("id", sa.Uuid(), primary_key=True)


def owner():
    return sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False)


def timestamp(name="created_at"):
    return sa.Column(name, sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)


def upgrade():
    op.create_table(
        "workers",
        identifier(),
        owner(),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("provider", sa.String(16), nullable=False),
        sa.Column("vcpu", sa.Integer(), nullable=False),
        sa.Column("ram_mb", sa.Integer(), nullable=False),
        sa.Column("disk_gb", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("ip", sa.String(45)),
        sa.Column("error_code", sa.String(80)),
        timestamp(),
        timestamp("updated_at"),
    )
    op.create_table(
        "worker_commands",
        identifier(),
        owner(),
        sa.Column("worker_id", sa.Uuid(), sa.ForeignKey("workers.id"), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("arguments", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("lease_id", sa.Uuid()),
        sa.Column("lease_until", sa.DateTime(timezone=True)),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        sa.Column("error_code", sa.String(80)),
        sa.Column("signature", sa.String(64), nullable=False),
        timestamp(),
        timestamp("updated_at"),
    )
    op.create_table(
        "worker_snapshots",
        identifier(),
        owner(),
        sa.Column("worker_id", sa.Uuid(), sa.ForeignKey("workers.id"), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("sha256", sa.String(64)),
        sa.Column("description", sa.Text()),
        timestamp(),
    )
    for table, columns in {
        "workers": ["user_id", "status"],
        "worker_commands": ["user_id", "worker_id", "status"],
        "worker_snapshots": ["user_id", "worker_id"],
    }.items():
        for column in columns:
            op.create_index(f"ix_{table}_{column}", table, [column])


def downgrade():
    for table in ["worker_snapshots", "worker_commands", "workers"]:
        op.drop_table(table)
