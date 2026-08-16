import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(30), nullable=False)
    severity = Column(String(20), nullable=False, default="moderate")
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)