"""
db/models/practice_sessions.py

Mirrors the `practice_sessions` table in db/schema/schema.sql. Backs FR-4
("create/track practice sessions"). One row per practice attempt-group; a
learner can retry multiple times within one session (see attempt_count).
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User
    from db.models.lessons import Lesson
    from db.models.assessments import Assessment
    from db.models.dynamic_sign_attempts import DynamicSignAttempt


class PracticeSession(Base):
    __tablename__ = "practice_sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('in_progress', 'completed', 'abandoned')",
            name="status_valid_values",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="in_progress")
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="practice_sessions")
    lesson: Mapped["Lesson"] = relationship(back_populates="practice_sessions")
    assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    dynamic_sign_attempts: Mapped[list["DynamicSignAttempt"]] = relationship(
    back_populates="practice_session",
    cascade="all, delete-orphan",
    )
    def __repr__(self) -> str:
        return f"<PracticeSession id={self.id} status={self.status!r}>"
