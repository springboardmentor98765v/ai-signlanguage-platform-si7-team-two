from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CertificateEligibilityResponse(BaseModel):
    learner_id: str
    eligible: bool
    average_score: float
    attempted_letters: List[str]
    missing_letters: List[str]
    attempts_count: int


class CertificateIssuedResponse(BaseModel):
    id: str
    learner_id: str
    average_score: float
    lessons_completed: int
    certificate_code: str
    issued_at: datetime
    is_valid: bool