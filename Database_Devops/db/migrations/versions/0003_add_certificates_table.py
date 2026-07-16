"""add certificates table

Revision ID: 0003_add_certificates_table
Revises: 0002_remaining_tables
Create Date: Milestone 2, Day 2
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0003_add_certificates_table"
down_revision = "0002_remaining_tables"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "certificates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "learner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("average_score", sa.Float(), nullable=False),
        sa.Column("lessons_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("certificate_code", sa.String(length=64), nullable=False),
        sa.Column("file_path", sa.String(length=255), nullable=True),
        sa.Column("issued_at", postgresql.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("is_valid", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.create_index("ix_certificates_learner_id", "certificates", ["learner_id"])
    op.create_index("ix_certificates_certificate_code", "certificates", ["certificate_code"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_certificates_certificate_code", table_name="certificates")
    op.drop_index("ix_certificates_learner_id", table_name="certificates")
    op.drop_table("certificates")
