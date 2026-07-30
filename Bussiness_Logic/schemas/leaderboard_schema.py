from pydantic import BaseModel
from uuid import UUID


class LeaderboardEntry(BaseModel):
    learner_id: UUID
    learner_name: str
    score: float
    rank: int

    model_config = {
        "from_attributes": True
    }