import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)
from database import Base

class CertificationExam(Base):
    __tablename__ = "certification_exams"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    learner_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    level = Column(String(20), nullable=False)
    score = Column(Numeric(5, 2), nullable=False)
    is_passed = Column(Boolean, nullable=False)
    taken_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
    certificate_id = Column(
        String(36),
        ForeignKey("certificates.id", ondelete="SET NULL"),
        nullable=True,
    )
