from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from database import Base


class AnalyticsSummary(Base):
    __tablename__ = "learner_analytics"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
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

    weak_letters = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    total_practice_time = Column(
        Integer,
        nullable=False,
        default=0,
    )

    last_updated = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )