"""add is_active column to users table

Revision ID: 0007_add_is_active_to_users
Revises: 0006_add_badges_streaks_notif
Create Date: Milestone 3, Day 7
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0007_add_is_active_to_users"
down_revision = "0006_add_badges_streaks_notif"
branch_labels = None
depends_on = None


def upgrade() -> None:
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
    op.drop_column("users", "is_active")
