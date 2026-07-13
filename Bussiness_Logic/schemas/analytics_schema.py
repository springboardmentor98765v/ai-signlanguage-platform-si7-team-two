from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class AnalyticsResponse(BaseModel):
    user_id: UUID
    average_accuracy: float
    lessons_completed: int
    total_practice_time: int
    weak_letters: List[str]
    last_updated: datetime