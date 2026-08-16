import uuid

from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    current_streak = Column(Integer, nullable=False, default=1)
    longest_streak = Column(Integer, nullable=False, default=1)
    last_practice_date = Column(Date, nullable=True)
