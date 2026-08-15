from uuid import UUID
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class TrainerLearnerResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    relationship: str


class TrainerEngagementResponse(BaseModel):
    total_practice_sessions: int
    completed_sessions: int
    total_attempts: int
    total_practice_time: int
    current_streak: int
    longest_streak: int


class TrainerSkillResponse(BaseModel):
    overall_average_accuracy: float
    recent_average_accuracy: float
    previous_average_accuracy: float
    weak_letters: List[str]
    improvement: float


class TrainerAssessmentResponse(BaseModel):
    total_assessments: int
    average_assessment_score: float
    highest_score: float
    lowest_score: float
    attempted_letters: List[str]
    weak_letters: List[str]


class CertificateDetailsResponse(BaseModel):
    certificate_code: str
    issued_at: datetime
    file_path: Optional[str] = None
    is_valid: bool


class TrainerCertificationResponse(BaseModel):
    certification_status: str
    average_score: float
    attempted_letters: List[str]
    completed_letters: List[str]
    missing_letters: List[str]
    certificate_earned: bool
    certificate_details: Optional[CertificateDetailsResponse] = None