from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.types import JSON

from database import Base


class AnalyticsSummary(Base):
    __tablename__ = "learner_analytics"

    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    average_accuracy = Column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    lessons_completed = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_practice_time = Column(
        Integer,
        nullable=False,
        default=0,
    )

    weak_letters = Column(
        JSON,
        nullable=False,
        default=list,
    )

    last_updated = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )