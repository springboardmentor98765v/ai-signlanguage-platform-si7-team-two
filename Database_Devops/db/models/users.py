"""
db/models/users.py

Mirrors the users table in db/schema/schema.sql.

Note:
password_hash is just a column here — actual hashing (bcrypt/passlib)
is handled by the backend layer. This model only stores whatever hash
string the backend provides.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.roles import Role
    from db.models.practice_sessions import PracticeSession
    from db.models.learner_analytics import LearnerAnalytics
    from db.models.certificates import Certificate
    from db.models.recommendations import Recommendation
    from db.models.notifications import Notification
    from db.models.streaks import Streak
    from db.models.badges import Badge
    from db.models.certification_exams import CertificationExam
    from db.models.accessibility_trainer_learner_mapping import AccessibilityTrainerLearnerMapping


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationships

    role: Mapped["Role"] = relationship(
        back_populates="users",
    )

    streak: Mapped["Streak | None"] = relationship(
        back_populates="learner",
        uselist=False,
        cascade="all, delete-orphan",
    )

    badges: Mapped[list["Badge"]] = relationship(
        back_populates="learner",
        cascade="all, delete-orphan",
    )

    practice_sessions: Mapped[list["PracticeSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    analytics: Mapped["LearnerAnalytics | None"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    certificates: Mapped[list["Certificate"]] = relationship(
        back_populates="learner",
        cascade="all, delete-orphan",
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="learner",
        cascade="all, delete-orphan",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    certification_exams: Mapped[list["CertificationExam"]] = relationship(
        back_populates="learner",
        cascade="all, delete-orphan",
    )

    trainer_mappings: Mapped[list["AccessibilityTrainerLearnerMapping"]] = relationship(
        "AccessibilityTrainerLearnerMapping",
        foreign_keys="[AccessibilityTrainerLearnerMapping.trainer_id]",
        back_populates="trainer",
        cascade="all, delete-orphan",
    )

    learner_mappings: Mapped[list["AccessibilityTrainerLearnerMapping"]] = relationship(
        "AccessibilityTrainerLearnerMapping",
        foreign_keys="[AccessibilityTrainerLearnerMapping.learner_id]",
        back_populates="learner",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"