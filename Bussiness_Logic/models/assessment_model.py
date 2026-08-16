from datetime import datetime
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)

from database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    session_id = Column(
        String(36),
        ForeignKey("practice_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    expected_sign = Column(
        String(2),
        nullable=False,
    )


    predicted_sign = Column(String(2), nullable=False)

    confidence = Column(Numeric(5, 4), nullable=False)

    hand_shape_score = Column(Numeric(5, 2), nullable=False)

    finger_position_score = Column(Numeric(5, 2), nullable=False)

    timing_score = Column(Numeric(5, 2), nullable=False)

    motion_score = Column(Numeric(5, 2), nullable=False)

    position_score = Column(Numeric(5, 2), nullable=False)

    overall_score = Column(Numeric(5, 2), nullable=False)

    is_correct = Column(Boolean, nullable=False)

    

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )