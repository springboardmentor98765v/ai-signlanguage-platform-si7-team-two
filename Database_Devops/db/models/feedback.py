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
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    assessment: Mapped["Assessment"] = relationship(back_populates="feedback_items")

    def __repr__(self) -> str:
        return f"<Feedback id={self.id} category={self.category!r}>"
