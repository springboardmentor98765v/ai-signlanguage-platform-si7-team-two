from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession
from models.assessment_model import Assessment
from models.feedback_model import Feedback
from services.scoring import calculate_scores
from services.feedback_rules import generate_feedback
from services.ai_client import get_ai_prediction
from uuid import UUID

router = APIRouter(prefix="/practice-flow", tags=["Full Pipeline (Day 7 Integration)"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit-attempt")
async def submit_attempt(
    session_id: UUID = Form(...),
    duration_seconds: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Get session
    session = db.query(PracticeSession).filter(PracticeSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Practice session not found")

    # 2. Call AI service (Intern 3) with the real image
    image_bytes = await file.read()
    ai_result = await get_ai_prediction(image_bytes, filename=file.filename)
    predicted_sign = ai_result["predicted_sign"]
    confidence = ai_result["confidence"]
    possible_issue = ai_result["possible_issue"]

    # 3. Log the attempt
    session.attempt_count += 1
    db.commit()

    # 4. Score it (Assessment Service)
    scores = calculate_scores(
        expected_sign=session.expected_sign,
        predicted_sign=predicted_sign,
        confidence=confidence,
        duration_seconds=duration_seconds
    )
    new_assessment = Assessment(
        session_id=session.id,
        predicted_sign=predicted_sign,
        expected_sign=session.expected_sign, 
        confidence=confidence,
        # expected_sign=expected_sign,
        hand_shape_score=scores["hand_shape_score"],
        finger_position_score=scores["finger_position_score"],
        timing_score=scores["timing_score"],
        motion_score=scores["motion_score"],
        position_score=scores["position_score"],
        overall_score=scores["overall_score"],
        is_correct=scores["is_correct"],
    )
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    # 5. Generate feedback (Feedback Service)
    rules_triggered = generate_feedback(scores, possible_issue)
    feedback_list = []
    for rule in rules_triggered:
        fb = Feedback(
            assessment_id=new_assessment.id,
            category=rule["category"],
            severity=rule["severity"] or "minor",  # DB requires NOT NULL
            message=rule["message"]
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)
        feedback_list.append({"category": fb.category, "severity": fb.severity, "message": fb.message})

    # 6. Return everything combined for Frontend (Intern 1)
    return {
        "session_id": str(session.id),
        "attempt_count": session.attempt_count,
        "predicted_sign": predicted_sign,
        "expected_sign": session.expected_sign,
        "confidence": confidence,
        "scores": scores,
        "feedback": feedback_list
    }