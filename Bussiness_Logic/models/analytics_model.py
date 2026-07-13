from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base
from datetime import datetime

class AnalyticsSummary(Base):
    __tablename__ = "analytics_summary"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    average_accuracy = Column(Numeric(5, 2), nullable=False, default=0)
    lessons_completed = Column(Integer, nullable=False, default=0)
    total_practice_time = Column(Integer, nullable=False, default=0)
    weak_letters = Column(JSONB, nullable=False, default=list)
    last_updated = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)