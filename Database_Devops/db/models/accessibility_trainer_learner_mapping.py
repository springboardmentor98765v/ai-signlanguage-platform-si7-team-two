from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User

class AccessibilityTrainerLearnerMapping(Base):
    __tablename__ = "accessibility_trainer_learner_mapping"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    trainer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assigned_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    trainer: Mapped["User"] = relationship(
        "User", foreign_keys=[trainer_id], back_populates="trainer_mappings"
    )
    learner: Mapped["User"] = relationship(
        "User", foreign_keys=[learner_id], back_populates="learner_mappings"
    )

    __table_args__ = (
        UniqueConstraint("trainer_id", "learner_id", name="uq_trainer_learner"),
    )

    def __repr__(self) -> str:
        return (
            f"<AccessibilityTrainerLearnerMapping trainer_id={self.trainer_id} "
            f"learner_id={self.learner_id}>"
        )
