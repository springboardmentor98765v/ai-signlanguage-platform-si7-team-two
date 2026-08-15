"""fix learner analytics table

Revision ID: 0008_fix_learner_analytics
Revises: 0007_add_is_active_to_users
Create Date: 2026-08-06
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "0008_fix_learner_analytics"
down_revision = "0007_add_is_active_to_users"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "learner_analytics",
        sa.Column(
            "total_practice_time",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.alter_column(
        "learner_analytics",
        "updated_at",
        new_column_name="last_updated",
    )


def downgrade():

    op.alter_column(
        "learner_analytics",
        "last_updated",
        new_column_name="updated_at",
    )

    op.drop_column(
        "learner_analytics",
        "total_practice_time",
    )