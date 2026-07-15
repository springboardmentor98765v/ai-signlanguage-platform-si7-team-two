from pydantic import BaseModel
class LessonResponse(BaseModel):
    id: int
    title: str
    letter: str