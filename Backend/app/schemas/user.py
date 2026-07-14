from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role_id: UUID

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
