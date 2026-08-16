from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.sql import func
import uuid

from app.database.database import Base

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)
    
    stars = Column(Integer, nullable=False, default=0) # 1-3 stars
    highest_accuracy = Column(Numeric(5, 2), nullable=False, default=0)
    
    is_completed = Column(Boolean, nullable=False, default=False)
    is_unlocked = Column(Boolean, nullable=False, default=False)
    
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
