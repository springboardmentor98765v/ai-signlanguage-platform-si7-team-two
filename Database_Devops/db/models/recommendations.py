"""
Recommendation model — Milestone 2, Day 2 deliverable.

Holds "you should practice this more" suggestions. Intern 4 builds the
actual rule engine on Day 4 (e.g. below 70% average over the last 3
attempts on a letter), but the table needs to exist first so that work
isn't blocked.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Which letter/word this recommendation is about.
    letter_or_word: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Plain-language reason, shown to the learner/instructor.
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # The accuracy that triggered this recommendation, for auditing.
    recent_avg_accuracy: Mapped[float | None] = mapped_column(nullable=True)
    
    # active -> still needs practice
    # completed -> learner practiced again and improved
    # dismissed -> learner or instructor dismissed it
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active", index=True)
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    learner: Mapped["User"] = relationship(back_populates="recommendations")

    def __repr__(self) -> str:
        return (
            f"<Recommendation id={self.id} learner_id={self.learner_id} "
            f"letter={self.letter_or_word!r} status={self.status!r}>"
        )
