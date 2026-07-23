import uuid
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base
from datetime import datetime

class AnalyticsSummary(Base):
    __tablename__ = "learner_analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    average_accuracy = Column(Numeric(5, 2), nullable=False, default=0)
    lessons_completed = Column(Integer, nullable=False, default=0)
    weak_letters = Column(JSONB, nullable=False, default=list)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)