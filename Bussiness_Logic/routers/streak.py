from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.streak_service import get_streak
from schemas.streak_schema import StreakOut
from uuid import UUID

router = APIRouter(prefix="/streak", tags=["Streak"])

@router.get("/{learner_id}", response_model=StreakOut)
def read_streak(learner_id: UUID, db: Session = Depends(get_db)):
    streak = get_streak(db, learner_id)
    if not streak:
        raise HTTPException(status_code=404, detail="No streak found for this learner")
    return streak