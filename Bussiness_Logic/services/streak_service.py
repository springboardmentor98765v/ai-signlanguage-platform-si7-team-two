from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID
from models.streak_model import Streak

def update_streak(
    db: Session,
    learner_id: UUID,
    practice_date: date,
) -> Streak:

    streak = (
        db.query(Streak)
        .filter(Streak.learner_id == learner_id)
        .first()
    )

    # First practice ever
    if streak is None:
        streak = Streak(
            learner_id=learner_id,
            current_streak=1,
            longest_streak=1,
            last_practice_date=practice_date,
        )

        db.add(streak)

    else:

        # No previous practice date
        if streak.last_practice_date is None:

            streak.current_streak = 1

        else:

            gap = (
                practice_date -
                streak.last_practice_date
            ).days

            # Already practiced today
            if gap == 0:
                pass

            # Yesterday
            elif gap == 1:
                streak.current_streak += 1

            # Missed one or more days
            else:
                streak.current_streak = 1

        streak.longest_streak = max(
            streak.longest_streak,
            streak.current_streak,
        )

        streak.last_practice_date = practice_date

    db.commit()
    db.refresh(streak)

    return streak

def get_streak(db: Session, learner_id: UUID) -> Streak | None:
    return db.query(Streak).filter(Streak.learner_id == learner_id).first()