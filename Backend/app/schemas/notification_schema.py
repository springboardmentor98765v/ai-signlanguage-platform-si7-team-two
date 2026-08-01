from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    user_id: UUID
    message: str


class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True