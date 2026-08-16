from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class NotificationCreate(BaseModel):
    user_id: UUID
    title: str = Field(min_length=3, max_length=100)
    message: str = Field(min_length=5, max_length=500)

    @field_validator("title", "message")
    @classmethod
    def remove_spaces(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationRead(BaseModel):
    is_read: bool = True
