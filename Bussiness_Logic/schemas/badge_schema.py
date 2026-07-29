from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BadgeOut(BaseModel):
    id: UUID
    learner_id: UUID
    badge_name: str
    earned_at: datetime

    model_config = {
        "from_attributes": True
    }