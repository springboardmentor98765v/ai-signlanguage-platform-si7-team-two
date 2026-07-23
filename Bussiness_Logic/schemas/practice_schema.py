from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class StartSessionRequest(BaseModel):
    user_id: UUID
    lesson_id: UUID

class StartSessionResponse(BaseModel):
    session_id: UUID
    status: str
    started_at: datetime

class EndSessionRequest(BaseModel):
    session_id: UUID

class EndSessionResponse(BaseModel):
    session_id: UUID
    status: str
    ended_at: datetime
    attempt_count: int