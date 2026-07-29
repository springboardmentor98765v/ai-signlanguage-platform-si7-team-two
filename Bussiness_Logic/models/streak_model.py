from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    learner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    current_streak = Column(
        Integer,
        nullable=False,
        default=1,
    )

    longest_streak = Column(
        Integer,
        nullable=False,
        default=1,
    )

    last_practice_date = Column(
        Date,
        nullable=True,
    )