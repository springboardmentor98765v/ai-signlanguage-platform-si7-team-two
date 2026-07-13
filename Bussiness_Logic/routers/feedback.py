from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.assessment_model import Assessment
from models.feedback_model import Feedback
from schemas.feedback_schema import FeedbackRequest, FeedbackResponse, FeedbackItem
from services.feedback_rules import generate_feedback

router = APIRouter(prefix="/feedback", tags=["Feedback Service"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate", response_model=FeedbackResponse)
def generate_feedback_for_assessment(request: FeedbackRequest, db: Session = Depends(get_db)):
    assessment = db.query(Assessment).filter(Assessment.id == request.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    scores = {
        "hand_shape_score": float(assessment.hand_shape_score),
        "finger_position_score": float(assessment.finger_position_score),
        "timing_score": float(assessment.timing_score),
        "motion_score": float(assessment.motion_score),
        "position_score": float(assessment.position_score),
        "overall_score": float(assessment.overall_score),
    }

    rules_triggered = generate_feedback(scores)

    saved_feedback = []
    for rule in rules_triggered:
        fb = Feedback(
            assessment_id=assessment.id,
            category=rule["category"],
            severity=rule["severity"],
            message=rule["message"]
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)
        saved_feedback.append(FeedbackItem(
            feedback_id=fb.id,
            category=fb.category,
            severity=fb.severity,
            message=fb.message,
            created_at=fb.created_at
        ))

    return FeedbackResponse(
        assessment_id=assessment.id,
        overall_score=float(assessment.overall_score),
        is_correct=assessment.is_correct,
        feedback=saved_feedback
    )