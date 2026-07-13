from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class StartSessionRequest(BaseModel):
    user_id: UUID
    lesson_id: UUID
    expected_sign: str

class StartSessionResponse(BaseModel):
    session_id: UUID
    status: str
    start_time: datetime

class EndSessionRequest(BaseModel):
    session_id: UUID

class EndSessionResponse(BaseModel):
    session_id: UUID
    status: str
    end_time: datetime
    attempt_count: int