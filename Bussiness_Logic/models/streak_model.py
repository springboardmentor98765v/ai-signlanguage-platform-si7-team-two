from sqlalchemy import Column, Integer, Date, ForeignKey, String
import uuid

from database import Base


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    learner_id = Column(
        String(36),
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