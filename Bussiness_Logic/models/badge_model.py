from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid

from database import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    learner_id = Column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
    )

    badge_name = Column(String, nullable=False)

    earned_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )