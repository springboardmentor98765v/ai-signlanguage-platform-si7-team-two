from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from database import Base


class AnalyticsSummary(Base):
    __tablename__ = "analytics_summary"

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
        JSONB,
        nullable=False,
        default=list,
    )

    last_updated = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )