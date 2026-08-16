from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class LessonCreate(BaseModel):
    course_id: UUID
    letter: str = Field(min_length=1, max_length=2)
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    reference_image_url: Optional[str] = None
    order_index: int = Field(gt=0)

    @field_validator("letter")
    @classmethod
    def validate_letter(cls, value):
        value = value.strip().upper()
        if not value:
            raise ValueError("Letter cannot be empty")
        return value


class LessonUpdate(BaseModel):
    letter: str = Field(min_length=1, max_length=2)
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    reference_image_url: Optional[str] = None
    order_index: int = Field(gt=0)

    @field_validator("letter")
    @classmethod
    def validate_letter(cls, value):
        value = value.strip().upper()
        if not value:
            raise ValueError("Letter cannot be empty")
        return value


class LessonResponse(BaseModel):
    id: UUID
    course_id: UUID
    letter: str
    title: str
    description: Optional[str] = None
    reference_image_url: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True
