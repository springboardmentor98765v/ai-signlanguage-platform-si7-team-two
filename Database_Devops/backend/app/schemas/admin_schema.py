from uuid import UUID
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    role_id: UUID

    class Config:
        from_attributes = True