from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.badge_service import get_badges
from schemas.badge_schema import BadgeOut
from uuid import UUID

router = APIRouter(prefix="/badges", tags=["Badges"])

@router.get("/{learner_id}", response_model=list[BadgeOut])
def read_badges(learner_id: UUID, db: Session = Depends(get_db)):
    return get_badges(db, learner_id)