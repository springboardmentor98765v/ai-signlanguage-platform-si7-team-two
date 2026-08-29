"""add dynamic sign attempts table

Revision ID: 0008_add_dynamic_sign_attempts
Revises: 0007_add_is_active_to_users
Create Date: Dynamic Sign Language Integration
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0008_add_dynamic_sign_attempts"
down_revision = "0007_add_is_active_to_users"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "dynamic_sign_attempts",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),

        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "practice_session_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "expected_word",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "predicted_word",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "is_correct",
            sa.Boolean(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["practice_session_id"],
            ["practice_sessions.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        "ix_dynamic_sign_attempts_user_id",
        "dynamic_sign_attempts",
        ["user_id"],
    )

    op.create_index(
        "ix_dynamic_sign_attempts_practice_session_id",
        "dynamic_sign_attempts",
        ["practice_session_id"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_dynamic_sign_attempts_practice_session_id",
        table_name="dynamic_sign_attempts",
    )

    op.drop_index(
        "ix_dynamic_sign_attempts_user_id",
        table_name="dynamic_sign_attempts",
    )

    op.drop_table(
        "dynamic_sign_attempts"
    )