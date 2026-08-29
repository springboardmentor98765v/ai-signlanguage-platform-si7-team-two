from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base


if TYPE_CHECKING:
    from db.models.users import User
    from db.models.practice_sessions import PracticeSession


class DynamicSignAttempt(Base):

    __tablename__ = "dynamic_sign_attempts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    practice_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "practice_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    expected_word: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    predicted_word: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    practice_session: Mapped["PracticeSession"] = relationship(
        back_populates="dynamic_sign_attempts"
    )

    def __repr__(self) -> str:
        return (
            f"<DynamicSignAttempt "
            f"id={self.id} "
            f"expected={self.expected_word!r} "
            f"predicted={self.predicted_word!r}>"
        )