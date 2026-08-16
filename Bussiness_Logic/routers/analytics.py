from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.practice_model import PracticeSession
from schemas.analytics_schema import AnalyticsResponse
from services.learner_analytics_service import (
    refresh_learner_analytics,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics Service"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/{user_id}",
    response_model=AnalyticsResponse,
)
def get_learner_analytics(
    user_id: str,
    db: Session = Depends(get_db),
):

    sessions = (
        db.query(PracticeSession)
        .filter(
            PracticeSession.user_id == user_id
        )
        .all()
    )

    if not sessions:
        raise HTTPException(
            status_code=404,
            detail="No practice sessions found for this user",
        )

    summary = refresh_learner_analytics(
        db,
        user_id,
    )

    return AnalyticsResponse(
        user_id=summary.user_id,
        average_accuracy=float(
            summary.average_accuracy
        ),
        lessons_completed=summary.lessons_completed,
        total_practice_time=summary.total_practice_time,
        weak_letters=summary.weak_letters,
        last_updated=summary.last_updated,
    )