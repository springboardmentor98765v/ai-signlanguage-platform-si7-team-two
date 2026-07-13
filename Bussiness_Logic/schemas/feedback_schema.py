from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class FeedbackRequest(BaseModel):
    assessment_id: UUID

class FeedbackItem(BaseModel):
    feedback_id: UUID
    category: str
    severity: Optional[str] = None
    message: str
    created_at: datetime

class FeedbackResponse(BaseModel):
    assessment_id: UUID
    overall_score: float
    is_correct: bool
    feedback: List[FeedbackItem]