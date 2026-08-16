from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from models.practice_model import User, PracticeSession
from models.assessment_model import Assessment
from models.streak_model import Streak
from schemas.leaderboard_schema import LeaderboardEntry


def get_leaderboard(
    db: Session,
    sort_by: str = "accuracy",
) -> List[LeaderboardEntry]:

    leaderboard = []

    if sort_by == "accuracy":

        results = (
            db.query(
                User.id,
                User.full_name,
                User.mascot_id,
                func.avg(Assessment.overall_score).label("score"),
            )
            .join(
                PracticeSession,
                PracticeSession.user_id == User.id,
            )
            .join(
                Assessment,
                Assessment.session_id == PracticeSession.id,
            )
            .group_by(
                User.id,
                User.full_name,
                User.mascot_id,
            )
            .order_by(
                func.avg(Assessment.overall_score).desc()
            )
            .all()
        )

    else:

        results = (
            db.query(
                User.id,
                User.full_name,
                User.mascot_id,
                Streak.current_streak.label("score"),
            )
            .join(
                Streak,
                Streak.learner_id == User.id,
            )
            .order_by(
                Streak.current_streak.desc()
            )
            .all()
        )

    for rank, learner in enumerate(results, start=1):
        raw_score = learner.score
        if raw_score is None:
            raw_score = 0.0

        leaderboard.append(
            LeaderboardEntry(
                learner_id=str(learner.id),
                learner_name=learner.full_name,
                score=float(raw_score),
                rank=rank,
                mascot_id=learner.mascot_id,
            )
        )

    return leaderboard