import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    average_score = Column(Numeric(5, 2), nullable=False)
    lessons_completed = Column(Integer, nullable=False, default=0)
    certificate_code = Column(String(64), nullable=False, unique=True)
    file_path = Column(String(255), nullable=True)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_valid = Column(Boolean, nullable=False, default=True)
