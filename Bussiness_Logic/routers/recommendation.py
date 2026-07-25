from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession, Recommendation
from models.assessment_model import Assessment
from services.recommendation_engine import find_weak_letters
from schemas.recommendation_schema import RecommendationResponse
from uuid import UUID

router = APIRouter(prefix="/recommendations", tags=["Recommendation Engine"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{learner_id}", response_model=RecommendationResponse)
def get_recommendations(learner_id: UUID, db: Session = Depends(get_db)):
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == learner_id).all()
    session_ids = [s.id for s in sessions]

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .all()
        if session_ids else []
    )

    weak_letters = find_weak_letters(assessments)
    weak_letter_names = {w["letter"] for w in weak_letters}

    # 1. Deactivate recommendations for letters that are no longer weak
    existing_recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.learner_id == learner_id,
            Recommendation.status == "active"
        )
        .all()
    )

    for rec in existing_recommendations:
        if rec.letter_or_word not in weak_letter_names:
            rec.status = "completed"

    # 2. Add new active recommendations for weak letters
    for w in weak_letters:
        existing = (
            db.query(Recommendation)
            .filter(
                Recommendation.learner_id == learner_id,
                Recommendation.letter_or_word == w["letter"],
                Recommendation.status == "active",
            )
            .first()
        )
        if not existing:
            new_rec = Recommendation(
                learner_id=learner_id,
                letter_or_word=w["letter"],
                reason=(
                         f"Practice the sign '{w['letter']}' again. "
                         f"Your recent average accuracy is {w['average_score']:.1f}%. "
                        "Keep practicing to improve your performance."
                       ),
                recent_avg_accuracy=w["average_score"],
                status="active",
            )
            db.add(new_rec)

    db.commit()

    # 3. Fetch and return active recommendations
    active_recs = (
        db.query(Recommendation)
        .filter(Recommendation.learner_id == learner_id, Recommendation.status == "active")
        .all()
    )

    return {
        "learner_id": str(learner_id),
        "recommendations": active_recs,
    }