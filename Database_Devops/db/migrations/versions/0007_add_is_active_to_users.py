"""add is_active column to users table

Revision ID: 0007_add_is_active_to_users
Revises: 0006_add_badges_streaks_notif
Create Date: Milestone 3, Day 7
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "0007_add_is_active_to_users"
down_revision = "0006_add_badges_streaks_notif"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    # 0001 already creates this column, so only add it
    # if it does not exist.
    if "is_active" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("true"),
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "is_active" in columns:
        op.drop_column("users", "is_active")