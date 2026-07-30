from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.leaderboard_schema import LeaderboardEntry
from services.leaderboard_service import get_leaderboard

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"],
)


@router.get(
    "/",
    response_model=List[LeaderboardEntry],
)
def leaderboard(
    sort_by: str = Query(
        "accuracy",
        pattern="^(accuracy|streak)$"
    ),
    db: Session = Depends(get_db),
):
    return get_leaderboard(
        db=db,
        sort_by=sort_by,
    )