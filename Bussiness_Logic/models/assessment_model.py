import uuid
from sqlalchemy import Column, String, Numeric, Boolean, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    session_id = Column(UUID(as_uuid=True), ForeignKey("practice_sessions.id", ondelete="CASCADE"), nullable=False)
    predicted_sign = Column(String(2), nullable=False)
    confidence = Column(Numeric(5, 4), nullable=False)
    expected_sign = Column(String(2), nullable=False)
    hand_shape_score = Column(Numeric(5, 2), nullable=False)
    finger_position_score = Column(Numeric(5, 2), nullable=False)
    timing_score = Column(Numeric(5, 2), nullable=False)
    motion_score = Column(Numeric(5, 2), nullable=False)
    position_score = Column(Numeric(5, 2), nullable=False)
    overall_score = Column(Numeric(5, 2), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)