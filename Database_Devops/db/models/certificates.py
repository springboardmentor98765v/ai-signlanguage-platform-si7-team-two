"""
Certificate model — Milestone 2, Day 2 deliverable.

Stores a record every time a learner earns a certificate. Intern 4 will
later fill in `average_score` / `lessons_completed` from the Assessment +
Analytics services and generate the actual PDF (Day 6-7); this table just
needs to exist and hold the resulting metadata + file reference.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.users import User
    from db.models.certification_exams import CertificationExam

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Snapshot of the numbers that made the learner eligible, so the
    # certificate stays accurate even if later attempts change the average.
    average_score: Mapped[float] = mapped_column(nullable=False)
    lessons_completed: Mapped[int] = mapped_column(nullable=False, server_default="0")
    
    # Unique human-shareable code printed on the certificate (e.g. for
    # verification), separate from the internal primary key.
    certificate_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    
    # Path/URL to the generated PDF once Intern 4 wires up ReportLab (Day 7).
    file_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    issued_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    
    # Lets an Admin revoke a certificate without deleting the historical row.
    is_valid: Mapped[bool] = mapped_column(nullable=False, server_default="true")

    learner: Mapped["User"] = relationship(back_populates="certificates")
    certification_exam: Mapped["CertificationExam | None"] = relationship(
        back_populates="certificate",
        uselist=False
    )

    def __repr__(self) -> str:
        return (
            f"<Certificate id={self.id} learner_id={self.learner_id} "
            f"code={self.certificate_code!r} valid={self.is_valid}>"
        )
