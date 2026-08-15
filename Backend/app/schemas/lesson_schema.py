from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class LessonCreate(BaseModel):
    course_id: UUID
    letter: str
    title: str
    description: Optional[str] = None
    reference_image_url: Optional[str] = None
    order_index: int


class LessonUpdate(BaseModel):
    letter: str
    title: str
    description: Optional[str] = None
    reference_image_url: Optional[str] = None
    order_index: int


class LessonResponse(BaseModel):
    id: str
    course_id: str
    letter: str
    title: str
    description: Optional[str] = None
    reference_image_url: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True

class LessonWithProgress(LessonResponse):
    status: str  # 'locked', 'current', or 'completed'
    stars: int = 0
    accuracy: float = 0.0

class LessonCompleteRequest(BaseModel):
    accuracy: float
