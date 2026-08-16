"""fix learner analytics table

Revision ID: 0008_fix_learner_analytics
Revises: 0007_add_is_active_to_users
Create Date: 2026-08-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers
revision = "0008_fix_learner_analytics"
down_revision = "0007_add_is_active_to_users"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("learner_analytics")
    }

    # total_practice_time may already exist because 0002
    # creates it as part of the original learner_analytics table.
    if "total_practice_time" not in columns:
        op.add_column(
            "learner_analytics",
            sa.Column(
                "total_practice_time",
                sa.Integer(),
                nullable=False,
                server_default="0",
            ),
        )

    # Rename updated_at to last_updated only if needed.
    if "updated_at" in columns and "last_updated" not in columns:
        op.alter_column(
            "learner_analytics",
            "updated_at",
            new_column_name="last_updated",
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("learner_analytics")
    }

    if "last_updated" in columns and "updated_at" not in columns:
        op.alter_column(
            "learner_analytics",
            "last_updated",
            new_column_name="updated_at",
        )

    if "total_practice_time" in columns:
        op.drop_column(
            "learner_analytics",
            "total_practice_time",
        )