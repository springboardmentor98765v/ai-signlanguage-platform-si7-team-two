"""add badges, streaks, and notifications tables

Revision ID: 0006_add_badges_streaks_notif
Revises: 0005_update_assessments_feedback
Create Date: Milestone 3, Day 6
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0006_add_badges_streaks_notif"
down_revision = "0005_update_assessments_feedback"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Create badges table
    op.create_table(
        "badges",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("badge_name", sa.String(100), nullable=False),
        sa.Column(
            "earned_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["learner_id"], ["users.id"], ondelete="CASCADE", name="fk_badges_user"
        ),
    )

    # 2. Create streaks table
    op.create_table(
        "streaks",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "learner_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            unique=True,
        ),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("longest_streak", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("last_practice_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["learner_id"], ["users.id"], ondelete="CASCADE", name="fk_streaks_user"
        ),
    )

    # 3. Create notifications table
    op.create_table(
        "notifications",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("message", sa.String(500), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_notifications_user"
        ),
    )

    # 4. Create indexes
    op.create_index(
        "ix_streaks_current_streak",
        "streaks",
        ["current_streak"],
        unique=False,
    )
    op.create_index(
        "ix_notifications_user_id_created_at",
        "notifications",
        ["user_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_notifications_user_id_created_at", table_name="notifications")
    op.drop_index("ix_streaks_current_streak", table_name="streaks")
    op.drop_table("notifications")
    op.drop_table("streaks")
    op.drop_table("badges")
