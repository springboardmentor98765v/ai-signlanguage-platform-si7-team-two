"""
db/models/streaks.py

Model for user practice streaks.
"""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import ForeignKey, Integer, Date, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User


class Streak(Base):
    __tablename__ = "streaks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    current_streak: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    longest_streak: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    last_practice_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    learner: Mapped["User"] = relationship(back_populates="streak")

    @property
    def user(self) -> User:
        return self.learner

    def __repr__(self) -> str:
        return f"<Streak id={self.id} learner_id={self.learner_id} current_streak={self.current_streak}>"
