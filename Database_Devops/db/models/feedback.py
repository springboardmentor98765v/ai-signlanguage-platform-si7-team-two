"""
db/models/feedback.py

Mirrors the `feedback` table in db/schema/schema.sql. Backs FR-4's
"rule-based feedback" — one assessment may generate several correction
messages, each tagged with a category matching the base doc's Step 8
examples (thumb position, finger extension, timing, etc.).
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.assessments import Assessment


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        CheckConstraint(
            # Allowed feedback categories per SRS FR-4 / base doc Step 8.
            #
            # NOTE — finger_position mapping (raised by Intern 3/Koushik, 17 Jul):
            # The AI engine's `possible_issue` field can return 'finger_position'
            # (e.g. finger curl or extension errors). That value is intentionally
            # mapped to 'hand_shape' in the feedback layer for now, since
            # 'hand_shape' is semantically broad enough to cover finger geometry.
            #
            # TODO: If a dedicated 'finger_position' category is ever needed,
            # add it here AND create an Alembic migration to update the DB
            # CHECK constraint (ALTER TABLE feedback DROP CONSTRAINT
            # category_valid_values; ALTER TABLE feedback ADD CONSTRAINT ...).
            "category IN ('hand_shape', 'timing', 'position', 'motion')",
            name="category_valid_values",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, server_default="moderate")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    assessment: Mapped["Assessment"] = relationship(back_populates="feedback_items")

    def __repr__(self) -> str:
        return f"<Feedback id={self.id} category={self.category!r}>"
