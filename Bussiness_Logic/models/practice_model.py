import uuid
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime

# --- Stub models: these tables already exist (created by Intern 5's schema.sql).
# We only declare minimal columns here so SQLAlchemy can resolve foreign keys.
# Do NOT add create_all logic for these — they are owned by Intern 5.

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(UUID(as_uuid=True), primary_key=True)


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="RESTRICT"), nullable=False)
    expected_sign = Column(String(2), nullable=False)
    status = Column(String(20), nullable=False, default="in_progress")
    attempt_count = Column(Integer, nullable=False, default=0)
    start_time = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime(timezone=True), nullable=True)
class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    learner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    letter_or_word = Column(String(50), nullable=False)
    reason = Column(String(255), nullable=False)
    recent_avg_accuracy = Column(Numeric(5, 2), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True), nullable=True)