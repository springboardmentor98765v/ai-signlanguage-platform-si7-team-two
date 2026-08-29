"""merge dynamic sign attempts and learner analytics heads

Revision ID: b7baf7fff16e
Revises: 0008_add_dynamic_sign_attempts, 0008_fix_learner_analytics
Create Date: 2026-08-29 17:29:28.316555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7baf7fff16e'
down_revision: Union[str, None] = ('0008_add_dynamic_sign_attempts', '0008_fix_learner_analytics')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
