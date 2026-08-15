from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func, text, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User
    from db.models.certificates import Certificate

class CertificationExam(Base):
    __tablename__ = "certification_exams"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    is_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    taken_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    certificate_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("certificates.id", ondelete="SET NULL"), nullable=True
    )

    learner: Mapped["User"] = relationship(back_populates="certification_exams")
    certificate: Mapped["Certificate"] = relationship(back_populates="certification_exam")

    def __repr__(self) -> str:
        return (
            f"<CertificationExam id={self.id} learner_id={self.learner_id} "
            f"level={self.level!r} score={self.score} passed={self.is_passed}>"
        )
