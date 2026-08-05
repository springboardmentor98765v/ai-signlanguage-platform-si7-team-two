"""Day 4: remaining tables (practice_sessions, assessments, feedback, learner_analytics)

This completes the schema formalized in Alembic — the same DDL already
reviewed in db/schema/schema.sql, for the 4 tables in Day 4's scope
(SRS §6, Intern 5, Day 4).

Revision ID: 0002_remaining_tables
Revises: 0001_initial_base_tables
Create Date: Day 4

IMPORTANT — same situation as migration 0001: your Day 2 database already
has these 4 tables (created via Docker's one-time init-script bootstrap).
Do NOT run `alembic upgrade head` against that existing database — it will
fail with "relation already exists". Instead:

    alembic stamp head

Only run `alembic upgrade head` for real on a genuinely fresh, empty
database with no prior bootstrap (e.g. CI, or a new teammate's local DB).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0002_remaining_tables"
down_revision: Union[str, None] = "0001_initial_base_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "practice_sessions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="in_progress"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "started_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("ended_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="fk_practice_sessions_user_id_users", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
            name="fk_practice_sessions_lesson_id_lessons",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "status IN ('in_progress', 'completed', 'abandoned')",
            name="status_valid_values",
        ),
    )
    op.create_index(
        "idx_sessions_user_id", "practice_sessions", ["user_id"]
    )
    op.create_index(
        "idx_sessions_lesson_id", "practice_sessions", ["lesson_id"]
    )

    op.create_table(
        "assessments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("predicted_sign", sa.String(2), nullable=False),
        sa.Column("confidence", sa.Numeric(5, 4), nullable=False),
        sa.Column("expected_sign", sa.String(2), nullable=False),
        sa.Column("accuracy_score", sa.Numeric(5, 2), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["practice_sessions.id"],
            name="fk_assessments_session_id_practice_sessions",
            ondelete="CASCADE",
        ),
        sa.CheckConstraint("confidence BETWEEN 0 AND 1", name="confidence_range"),
        sa.CheckConstraint(
            "accuracy_score BETWEEN 0 AND 100", name="accuracy_score_range"
        ),
    )
    op.create_index("idx_assessments_session_id", "assessments", ["session_id"])

    op.create_table(
        "feedback",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("assessment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["assessments.id"],
            name="fk_feedback_assessment_id_assessments",
            ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "category IN ('hand_shape', 'timing', 'position', 'motion')",
            name="category_valid_values",
        ),
    )
    op.create_index("idx_feedback_assessment_id", "feedback", ["assessment_id"])

    op.create_table(
        "learner_analytics",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("average_accuracy", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("lessons_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("weak_letters", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("total_practice_time", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "last_updated",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="fk_learner_analytics_user_id_users", ondelete="CASCADE"
        ),
        sa.UniqueConstraint("user_id", name="uq_learner_analytics_user_id"),
    )


def downgrade() -> None:
    op.drop_table("learner_analytics")
    op.drop_index("idx_feedback_assessment_id", table_name="feedback")
    op.drop_table("feedback")
    op.drop_index("idx_assessments_session_id", table_name="assessments")
    op.drop_table("assessments")
    op.drop_index("idx_sessions_lesson_id", table_name="practice_sessions")
    op.drop_index("idx_sessions_user_id", table_name="practice_sessions")
    op.drop_table("practice_sessions")
