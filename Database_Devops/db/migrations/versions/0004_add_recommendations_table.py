"""add recommendations table

Revision ID: 0004_add_recommendations_table
Revises: 0003_add_certificates_table
Create Date: Milestone 2, Day 2
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0004_add_recommendations_table"
down_revision = "0003_add_certificates_table"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "learner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("letter_or_word", sa.String(length=50), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("recent_avg_accuracy", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("resolved_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index("ix_recommendations_learner_id", "recommendations", ["learner_id"])
    op.create_index("ix_recommendations_status", "recommendations", ["status"])


def downgrade() -> None:
    op.drop_index("ix_recommendations_status", table_name="recommendations")
    op.drop_index("ix_recommendations_learner_id", table_name="recommendations")
    op.drop_table("recommendations")
