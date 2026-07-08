from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StartSessionRequest(BaseModel):
    user_id: int
    lesson_id: int
    expected_sign: str

class StartSessionResponse(BaseModel):
    session_id: int
    status: str
    start_time: datetime

class EndSessionRequest(BaseModel):
    session_id: int

class EndSessionResponse(BaseModel):
    session_id: int
    status: str
    end_time: datetime
    attempt_count: int