"""add certification_exams table

Revision ID: 0010_add_certification_exams
Revises: 0009_add_lesson_progress
Create Date: 2026-09-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0010_add_certification_exams"
down_revision: Union[str, None] = "0009_add_lesson_progress"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS certification_exams (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            learner_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            level varchar(20) NOT NULL,
            score numeric(5,2) NOT NULL,
            is_passed boolean NOT NULL,
            taken_at timestamp with time zone NOT NULL DEFAULT now(),
            certificate_id uuid REFERENCES certificates(id) ON DELETE SET NULL
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_certification_exams_learner_id
        ON certification_exams(learner_id)
        """
    )


def downgrade() -> None:
    pass
