from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class RecommendationItem(BaseModel):
    id: UUID
    letter_or_word: str
    reason: str
    recent_avg_accuracy: Optional[float] = None
    status: str
    created_at: datetime


class RecommendationResponse(BaseModel):
    learner_id: str
    recommendations: List[RecommendationItem]