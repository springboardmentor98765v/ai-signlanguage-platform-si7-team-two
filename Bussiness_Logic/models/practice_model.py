import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)
from database import Base


# -------------------------
# Stub Models (mirror the actual DB tables from Database_Devops)
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    full_name = Column(String(120), nullable=False)
    mascot_id = Column(String(50), nullable=True, default="owl")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(36), primary_key=True)
    letter = Column(String(2), nullable=False)


# -------------------------
# Practice Session
# -------------------------

class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),  # Works on SQLite and PostgreSQL
    )

    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    lesson_id = Column(
        String(36),
        ForeignKey("lessons.id", ondelete="RESTRICT"),
        nullable=False,
    )

    expected_sign = Column(String(2), nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="in_progress",
    )

    attempt_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    ended_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


# -------------------------
# Recommendation
# -------------------------

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    learner_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    letter_or_word = Column(String(50), nullable=False)

    reason = Column(String(255), nullable=False)

    recent_avg_accuracy = Column(Numeric(5, 2), nullable=True)

    status = Column(
        String(20),
        nullable=False,
        default="active",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


# -------------------------
# Certificate
# -------------------------

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    learner_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    average_score = Column(Numeric(5, 2), nullable=False)

    lessons_completed = Column(Integer, nullable=False)

    certificate_code = Column(String(64), unique=True, nullable=False)

    file_path = Column(String(255))

    issued_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    is_valid = Column(Boolean, nullable=False, default=True)