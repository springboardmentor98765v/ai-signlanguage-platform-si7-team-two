from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.database.database import Base


class AnalyticsSummary(Base):
    """Aggregated learner analytics stored in PostgreSQL's analytics_summary table."""

    __tablename__ = "analytics_summary"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    average_accuracy = Column(Numeric(5, 2), nullable=False, default=0)
    lessons_completed = Column(Integer, nullable=False, default=0)
    total_practice_time = Column(Integer, nullable=False, default=0)
    weak_letters = Column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    last_updated = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
