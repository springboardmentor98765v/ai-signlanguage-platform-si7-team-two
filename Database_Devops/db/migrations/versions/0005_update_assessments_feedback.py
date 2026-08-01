"""update assessments and feedback tables with subscores and severity

Revision ID: 0005_update_assessments_feedback
Revises: 0004_add_recommendations_table
Create Date: Milestone 2, Day 3
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0005_update_assessments_feedback"
down_revision = "0004_add_recommendations_table"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Update assessments table
    op.execute("ALTER TABLE assessments DROP CONSTRAINT IF EXISTS accuracy_score_range")
    op.alter_column("assessments", "accuracy_score", new_column_name="overall_score")
    
    op.add_column("assessments", sa.Column("hand_shape_score", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("assessments", sa.Column("finger_position_score", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("assessments", sa.Column("timing_score", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("assessments", sa.Column("motion_score", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("assessments", sa.Column("position_score", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("assessments", sa.Column("is_correct", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    
    op.execute("ALTER TABLE assessments ADD CONSTRAINT overall_score_range CHECK (overall_score >= 0 AND overall_score <= 100)")

    # 2. Update feedback table
    op.add_column("feedback", sa.Column("severity", sa.String(length=20), nullable=False, server_default="moderate"))


def downgrade() -> None:
    # 1. Revert feedback table
    op.drop_column("feedback", "severity")

    # 2. Revert assessments table
    op.execute("ALTER TABLE assessments DROP CONSTRAINT IF EXISTS overall_score_range")
    op.drop_column("assessments", "is_correct")
    op.drop_column("assessments", "position_score")
    op.drop_column("assessments", "motion_score")
    op.drop_column("assessments", "timing_score")
    op.drop_column("assessments", "finger_position_score")
    op.drop_column("assessments", "hand_shape_score")
    
    op.alter_column("assessments", "overall_score", new_column_name="accuracy_score")
    op.execute("ALTER TABLE assessments ADD CONSTRAINT accuracy_score_range CHECK (accuracy_score >= 0 AND accuracy_score <= 100)")
