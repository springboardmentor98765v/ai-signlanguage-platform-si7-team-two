from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
import uuid

from app.database.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    letter = Column(String(2), nullable=False)
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    reference_image_url = Column(String(500), nullable=True)
    order_index = Column(Integer, nullable=False, default=0)
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
