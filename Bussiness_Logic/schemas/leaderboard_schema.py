from pydantic import BaseModel
from typing import Optional

class LeaderboardEntry(BaseModel):
    learner_id: str
    learner_name: str
    score: float
    rank: int
    mascot_id: Optional[str] = "owl"

    model_config = {
        "from_attributes": True
    }