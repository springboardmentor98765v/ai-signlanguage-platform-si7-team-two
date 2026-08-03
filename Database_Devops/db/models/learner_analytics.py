"""
db/models/learner_analytics.py

Mirrors the `learner_analytics` table in db/schema/schema.sql. Backs FR-4's
"aggregate basic analytics per learner" — one summary row per user.

Scope note: only the 3 fields SRS Day 6 (Intern 4) actually asks for
(average_accuracy, lessons_completed, weak_letters) exist here. Fields like
"improvement_rate" or "recommended_lessons" from the fuller base document
are explicitly out of scope for Milestone 1 (SRS §1.4: "advanced
analytics/recommendations" deferred) — see db/BASE_DOCUMENT_ALIGNMENT.md.
Do not add them without a scope decision from the team.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User


class LearnerAnalytics(Base):
    __tablename__ = "learner_analytics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    average_accuracy: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    lessons_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    weak_letters: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="analytics")

    def __repr__(self) -> str:
        return f"<LearnerAnalytics user_id={self.user_id} average_accuracy={self.average_accuracy}>"
