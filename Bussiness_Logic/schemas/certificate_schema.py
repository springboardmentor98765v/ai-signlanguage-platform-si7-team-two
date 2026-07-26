from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class CertificateEligibilityResponse(BaseModel):
    learner_id: str
    eligible: bool
    average_score: float
    attempted_letters: List[str]
    missing_letters: List[str]
    attempts_count: int


class CertificateIssuedResponse(BaseModel):
    id: UUID
    learner_id: UUID
    average_score: float
    lessons_completed: int
    certificate_code: str
    issued_at: datetime
    is_valid: bool