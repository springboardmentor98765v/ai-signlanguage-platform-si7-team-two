from pydantic import BaseModel
from uuid import UUID
from datetime import date


class StreakOut(BaseModel):
    id: UUID
    learner_id: UUID
    current_streak: int
    longest_streak: int
    last_practice_date: date | None

    model_config = {
        "from_attributes": True
    }