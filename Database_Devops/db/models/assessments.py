"""
db/models/assessments.py

Mirrors the `assessments` table in db/schema/schema.sql. Field names
(predicted_sign, confidence) deliberately match Intern 3's AI service
response shape per FR-3, so no translation layer is needed between the AI
service and this table.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.practice_sessions import PracticeSession
    from db.models.feedback import Feedback


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (
        CheckConstraint("confidence BETWEEN 0 AND 1", name="confidence_range"),
        CheckConstraint("accuracy_score BETWEEN 0 AND 100", name="accuracy_score_range"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("practice_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    predicted_sign: Mapped[str] = mapped_column(String(2), nullable=False)
    confidence: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    expected_sign: Mapped[str] = mapped_column(String(2), nullable=False)
    accuracy_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    session: Mapped["PracticeSession"] = relationship(back_populates="assessments")
    feedback_items: Mapped[list["Feedback"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Assessment id={self.id} predicted_sign={self.predicted_sign!r} accuracy={self.accuracy_score}>"
