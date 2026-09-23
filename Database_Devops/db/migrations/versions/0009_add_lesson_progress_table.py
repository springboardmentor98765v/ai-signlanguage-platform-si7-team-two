"""add lesson_progress table

Revision ID: 0009_add_lesson_progress
Revises: b7baf7fff16e
Create Date: 2026-09-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0009_add_lesson_progress"
down_revision: Union[str, None] = "b7baf7fff16e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lesson_progress",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("highest_accuracy", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("is_completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_unlocked", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("completed_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_lesson_progress_user_id_users",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
            name="fk_lesson_progress_lesson_id_lessons",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_lesson_progress_user_lesson"),
    )
    op.create_index("idx_lesson_progress_user_id", "lesson_progress", ["user_id"])
    op.create_index("idx_lesson_progress_lesson_id", "lesson_progress", ["lesson_id"])


def downgrade() -> None:
    op.drop_index("idx_lesson_progress_lesson_id", table_name="lesson_progress")
    op.drop_index("idx_lesson_progress_user_id", table_name="lesson_progress")
    op.drop_table("lesson_progress")
