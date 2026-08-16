from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    full_name: str = Field(min_length=3, max_length=120, examples=["John Doe"])

    email: EmailStr = Field(examples=["john@example.com"])

    password: str = Field(min_length=8, max_length=100, examples=["Password@123"])

    role: str = Field(default="learner", examples=["learner"])

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Full name cannot be empty")

        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        allowed = {
            "learner",
            "instructor",
            "trainer",
            "admin",
        }

        normalized = value.strip().lower()

        if normalized not in allowed:
            raise ValueError(
                f"Invalid role '{value}'. "
                "Must be one of: learner, instructor, trainer, admin."
            )

        return normalized.capitalize()


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


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


class UpdateProfile(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)

    email: EmailStr

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
