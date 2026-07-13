from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.assessment_model import Assessment
from models.practice_model import PracticeSession
from schemas.assessment_schema import AssessmentRequest, AssessmentResponse
from services.scoring import calculate_scores

router = APIRouter(prefix="/assessment", tags=["Assessment Service"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/evaluate", response_model=AssessmentResponse)
def evaluate_attempt(request: AssessmentRequest, db: Session = Depends(get_db)):
    session = db.query(PracticeSession).filter(PracticeSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Practice session not found")

    scores = calculate_scores(
        expected_sign=request.expected_sign,
        predicted_sign=request.predicted_sign,
        confidence=request.confidence,
        duration_seconds=request.duration_seconds
    )

    new_assessment = Assessment(
        session_id=request.session_id,
        predicted_sign=request.predicted_sign,
        confidence=request.confidence,
        hand_shape_score=scores["hand_shape_score"],
        finger_position_score=scores["finger_position_score"],
        timing_score=scores["timing_score"],
        motion_score=scores["motion_score"],
        position_score=scores["position_score"],
        overall_score=scores["overall_score"],
        is_correct=scores["is_correct"]
    )
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return AssessmentResponse(
        assessment_id=new_assessment.id,
        session_id=new_assessment.session_id,
        predicted_sign=new_assessment.predicted_sign,
        confidence=float(new_assessment.confidence),
        hand_shape_score=float(new_assessment.hand_shape_score),
        finger_position_score=float(new_assessment.finger_position_score),
        timing_score=float(new_assessment.timing_score),
        motion_score=float(new_assessment.motion_score),
        position_score=float(new_assessment.position_score),
        overall_score=float(new_assessment.overall_score),
        is_correct=new_assessment.is_correct,
        created_at=new_assessment.created_at
    )