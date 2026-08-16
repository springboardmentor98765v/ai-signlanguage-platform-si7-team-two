from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    full_name: str = Field(
        min_length=3,
        max_length=120,
        examples=["John Doe"]
    )
    email: EmailStr = Field(
        examples=["john@example.com"]
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        examples=["Password@123"]
    )

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Full name cannot be empty")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role_id: str
    mascot_id: Optional[str] = "owl"

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UpdateProfile(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    mascot_id: Optional[str] = "owl"

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Full name cannot be empty")
        return value

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Full name cannot be empty")
        return value


class ChangePassword(BaseModel):
    old_password: str = Field(min_length=8, max_length=100)
    new_password: str = Field(min_length=8, max_length=100)


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    new_password: str = Field(min_length=8, max_length=100)
