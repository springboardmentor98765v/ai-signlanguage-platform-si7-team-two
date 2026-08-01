from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class CertificateSummary(BaseModel):
    certificate_code: str
    average_score: float
    issued_at: Optional[datetime] = None

class ProgressReportResponse(BaseModel):
    user_id: UUID
    full_name: Optional[str] = None
    lessons_completed: int
    total_practice_time: int
    average_accuracy: float
    attempted_letters: List[str]
    weak_letters: List[str]
    total_attempts: int
    certificates_earned: List[CertificateSummary]
    generated_at: datetime