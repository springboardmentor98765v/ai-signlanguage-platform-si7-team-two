from uuid import UUID

from pydantic import BaseModel, Field


class DynamicSignAttemptCreate(BaseModel):

    user_id: UUID

    practice_session_id: UUID

    expected_word: str = Field(
        min_length=1,
        max_length=50,
    )

    predicted_word: str = Field(
        min_length=1,
        max_length=50,
    )

    confidence: float = Field(
        ge=0,
        le=100,
    )


class DynamicSignAttemptResponse(BaseModel):

    id: UUID

    user_id: UUID

    practice_session_id: UUID

    expected_word: str

    predicted_word: str

    confidence: float

    is_correct: bool

    class Config:
        from_attributes = True