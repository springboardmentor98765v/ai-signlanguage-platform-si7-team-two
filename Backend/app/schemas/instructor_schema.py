from uuid import UUID
from typing import List

from pydantic import BaseModel, EmailStr


class StudentResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class StudentProgressResponse(BaseModel):
    average_accuracy: float
    lessons_completed: int
    weak_letters: List[str]

    class Config:
        from_attributes = True


class AssessmentResponse(BaseModel):
    id: UUID
    session_id: UUID
    predicted_sign: str
    expected_sign: str
    overall_score: float
    is_correct: bool

    class Config:
        from_attributes = True