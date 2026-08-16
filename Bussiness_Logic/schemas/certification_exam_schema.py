from pydantic import BaseModel
from typing import List


class CertificationExamRequest(BaseModel):
    level: str
    scores: List[float]


class CertificationExamResponse(BaseModel):
    level: str
    total_signs: int
    average_score: float
    threshold: float
    passed: bool