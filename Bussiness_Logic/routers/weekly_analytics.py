from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession
from models.assessment_model import Assessment
from services.weekly_analytics_engine import compute_weekly_stats
from schemas.weekly_analytics_schema import WeeklyAnalyticsResponse
from uuid import UUID

router = APIRouter(prefix="/weekly-analytics", tags=["Weekly Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}", response_model=WeeklyAnalyticsResponse)
def get_weekly_analytics(user_id: UUID, db: Session = Depends(get_db)):
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == user_id).all()
    session_ids = [s.id for s in sessions]

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .all()
        if session_ids else []
    )

    weekly_stats = compute_weekly_stats(assessments)

    return {
        "user_id": str(user_id),
        "weekly_stats": weekly_stats,
    }