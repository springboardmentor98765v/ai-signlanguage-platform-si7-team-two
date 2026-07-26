from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from uuid import UUID

from database import SessionLocal
from models.assessment_model import Assessment
from models.feedback_model import Feedback
from models.practice_model import PracticeSession, Lesson, Recommendation
from schemas.assessment_schema import AssessmentRequest, AssessmentResponse
from services.recommendation_engine import find_weak_letters
from services.scoring import calculate_scores, normalize_confidence

router = APIRouter(prefix="/assessment", tags=["Assessment Service"])


class ScoreRequest(BaseModel):
    session_id: UUID | None = None
    expected_sign: str = Field(min_length=1, max_length=2)
    predicted_sign: str = Field(min_length=1, max_length=2)
    confidence: float = Field(ge=0, le=100)
    attempt_duration: float = Field(default=0.0, ge=0)


def assessment_status(accuracy: float) -> str:
    if accuracy >= 90:
        return "Excellent"
    if accuracy >= 80:
        return "Very Good"
    if accuracy >= 60:
        return "Good"
    if accuracy >= 40:
        return "Needs Practice"
    return "Try Again"


def assessment_feedback(scores: dict, is_correct: bool, confidence: float) -> list[str]:
    feedback = []
    if not is_correct:
        feedback.append("Incorrect sign detected. Practice the reference image.")
    if scores["overall_score"] >= 90:
        feedback.append("Excellent hand posture.")
    if confidence < 60:
        feedback.append("Hold your hand steady.")
    if scores["overall_score"] < 50:
        feedback.append("Practice finger placement.")
    if scores["finger_position_score"] < 70 and is_correct:
        feedback.append("Keep your thumb closer to the palm.")
    if confidence > 95:
        feedback.append("Excellent consistency.")
    return feedback or ["Good hand shape. Keep practicing for consistency."]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/score")
def score_attempt(request: ScoreRequest, db: Session = Depends(get_db)):
    """Score an attempt and persist it when the frontend provides a session ID."""
    expected_sign = request.expected_sign.strip().upper()
    predicted_sign = request.predicted_sign.strip().upper()
    confidence = normalize_confidence(request.confidence)
    scores = calculate_scores(
        expected_sign=expected_sign,
        predicted_sign=predicted_sign,
        confidence=confidence,
        duration_seconds=request.attempt_duration,
    )
    accuracy = scores["overall_score"]
    is_correct = expected_sign == predicted_sign
    feedback_messages = assessment_feedback(scores, is_correct, confidence)
    completed_at = datetime.now(timezone.utc)
    assessment_id = None

    if request.session_id:
        session = db.query(PracticeSession).filter(PracticeSession.id == request.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Practice session not found")
        
        lesson = db.query(Lesson).filter(Lesson.id == session.lesson_id).first()
        if not lesson or lesson.letter.strip().upper() != expected_sign:
            raise HTTPException(status_code=400, detail="Expected sign does not match the practice session's lesson")
        
        new_assessment = Assessment(
            session_id=session.id,
            predicted_sign=predicted_sign,
            confidence=confidence / 100,
            hand_shape_score=scores["hand_shape_score"],
            finger_position_score=scores["finger_position_score"],
            timing_score=scores["timing_score"],
            motion_score=scores["motion_score"],
            position_score=scores["position_score"],
            overall_score=accuracy,
            is_correct=is_correct,
        )
        db.add(new_assessment)
        db.flush()

        for message in feedback_messages:
            db.add(Feedback(
                assessment_id=new_assessment.id,
                category="hand_shape",
                severity="moderate",
                message=message,
            ))

        session.attempt_count += 1
        db.commit()
        db.refresh(new_assessment)

        # ------------------------------
        # Auto-update Recommendations
        # ------------------------------
        assessment_session_pairs = (
            db.query(Assessment, PracticeSession)
            .join(
                PracticeSession,
                Assessment.session_id == PracticeSession.id
            )
            .filter(
                PracticeSession.user_id == session.user_id
            )
            .all()
        )

        weak_letters = find_weak_letters(assessment_session_pairs)
        weak_letter_names = {w["letter"] for w in weak_letters}

        # Mark improved recommendations as completed
        existing_recommendations = (
            db.query(Recommendation)
            .filter(
                Recommendation.learner_id == session.user_id,
                Recommendation.status == "active",
            )
            .all()
        )

        for rec in existing_recommendations:
            if rec.letter_or_word not in weak_letter_names:
                rec.status = "completed"

        # Add new recommendations
        for w in weak_letters:
            existing = (
                db.query(Recommendation)
                .filter(
                    Recommendation.learner_id == session.user_id,
                    Recommendation.letter_or_word == w["letter"],
                    Recommendation.status == "active",
                )
                .first()
            )

            if not existing:
                db.add(
                    Recommendation(
                        learner_id=session.user_id,
                        letter_or_word=w["letter"],
                        reason=(
                                f"Practice the sign '{w['letter']}' again. "
                                f"Your recent average accuracy is {w['average_score']:.1f}%. "
                                "Keep practicing to improve your performance."
                            ),
                        recent_avg_accuracy=w["average_score"],
                        status="active",
                    )
                )

        db.commit()

        assessment_id = str(new_assessment.id)
        completed_at = new_assessment.created_at

    return {
        "assessment_id": assessment_id,
        "session_id": str(request.session_id) if request.session_id else None,
        "expected_sign": expected_sign,
        "predicted_sign": predicted_sign,
        "confidence": round(confidence, 2),
        "accuracy": accuracy,
        "status": assessment_status(accuracy),
        "is_correct": is_correct,
        "attempt_duration": round(request.attempt_duration, 2),
        "completed_at": completed_at.isoformat(),
        "feedback": feedback_messages,
    }