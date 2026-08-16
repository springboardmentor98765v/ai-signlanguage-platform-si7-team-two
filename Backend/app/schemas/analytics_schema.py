from typing import List

from pydantic import BaseModel, ConfigDict


class AnalyticsSummaryResponse(BaseModel):
    average_accuracy: float
    lessons_completed: int
    total_practice_time: int
    weak_letters: List[str]

    model_config = ConfigDict(from_attributes=True)
