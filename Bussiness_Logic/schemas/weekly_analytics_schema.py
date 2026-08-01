from pydantic import BaseModel
from typing import List, Optional


class WeeklyStat(BaseModel):
    week_start: str
    average_accuracy: float
    improvement_rate: Optional[float] = None
    weak_letters: List[str]
    attempts_count: int


class WeeklyAnalyticsResponse(BaseModel):
    user_id: str
    weekly_stats: List[WeeklyStat]