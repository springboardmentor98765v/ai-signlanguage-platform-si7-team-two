"""
db/models/lessons.py

Mirrors the `lessons` table in db/schema/schema.sql — the "Modules" named
in SRS FR-2 ("CRUD APIs for Lessons/Modules"). One row per target sign
(e.g. letter "A") within a course.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.courses import Course
    from db.models.practice_sessions import PracticeSession


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    letter: Mapped[str] = mapped_column(String(2), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    course: Mapped["Course"] = relationship(back_populates="lessons")
    practice_sessions: Mapped[list["PracticeSession"]] = relationship(back_populates="lesson")

    def __repr__(self) -> str:
        return f"<Lesson id={self.id} letter={self.letter!r}>"
