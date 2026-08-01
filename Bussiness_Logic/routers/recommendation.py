from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession
from models.assessment_model import Assessment
from models.practice_model import Recommendation
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
                reason=f"Average accuracy on '{w['letter']}' dropped below 70% over last 3 attempts.",
                recent_avg_accuracy=w["average_score"],
                status="active",
            )
            db.add(new_rec)
    db.commit()

    active_recs = (
        db.query(Recommendation)
        .filter(Recommendation.learner_id == learner_id, Recommendation.status == "active")
        .all()
    )

    return {
        "learner_id": str(learner_id),
        "recommendations": active_recs,
    }
