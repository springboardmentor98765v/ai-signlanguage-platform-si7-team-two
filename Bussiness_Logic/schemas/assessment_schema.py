from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AssessmentRequest(BaseModel):
    session_id: UUID
    expected_sign: str
    predicted_sign: str        # from Intern 3 (mocked for now)
    confidence: float          # 0.0 to 1.0, from Intern 3 (mocked for now)
    duration_seconds: float    # how long the learner held the gesture

class AssessmentResponse(BaseModel):
    assessment_id: UUID
    session_id: UUID
    predicted_sign: str
    confidence: float
    hand_shape_score: float
    finger_position_score: float
    timing_score: float
    motion_score: float
    position_score: float
    overall_score: float
    is_correct: bool
    created_at: datetime