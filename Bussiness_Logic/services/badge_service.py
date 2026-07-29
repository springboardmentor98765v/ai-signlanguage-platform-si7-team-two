from sqlalchemy.orm import Session
from uuid import UUID
from models.badge_model import Badge
from models.practice_model import PracticeSession
from models.assessment_model import Assessment
from services.streak_service import get_streak


def _get_sessions(db: Session, user_id: UUID) -> list:
    return db.query(PracticeSession).filter(PracticeSession.user_id == user_id).all()


def _get_assessments_with_letter(db: Session, user_id: UUID) -> list:
    """Returns (Assessment, expected_letter) pairs via join on PracticeSession."""
    return (
        db.query(Assessment, PracticeSession.expected_sign)
        .join(PracticeSession, Assessment.session_id == PracticeSession.id)
        .filter(PracticeSession.user_id == user_id)
        .all()
    )


def check_alphabet_master(db: Session, user_id: UUID) -> bool:
    rows = _get_assessments_with_letter(db, user_id)
    if not rows:
        return False
    attempted_letters = {expected_sign for _, expected_sign in rows}
    avg_score = sum(float(a.overall_score) for a, _ in rows) / len(rows)
    return (
    len(attempted_letters) == 26
    and avg_score >= 80.0
)

def check_consistency_streak(db: Session, user_id: UUID) -> bool:
    streak = get_streak(db, user_id)
    return streak is not None and streak.current_streak >= 7


def check_first_steps(db: Session, user_id: UUID) -> bool:
    completed = [s for s in _get_sessions(db, user_id) if s.status == "completed"]
    return len(completed) >= 1


BADGE_RULES = {
    "Alphabet Master": check_alphabet_master,
    "7-Day Streak": check_consistency_streak,
    "First Steps": check_first_steps,
}


def evaluate_badges(db: Session, user_id: UUID) -> list[str]:
    newly_earned = []
    for name, rule_fn in BADGE_RULES.items():
        exists = db.query(Badge).filter_by(learner_id=user_id, badge_name=name).first()
        if not exists and rule_fn(db, user_id):
            db.add(Badge(learner_id=user_id, badge_name=name))
            newly_earned.append(name)
    if newly_earned:
        db.commit()
    return newly_earned


def get_badges(db: Session, user_id: UUID) -> list[Badge]:
    return db.query(Badge).filter(Badge.learner_id == user_id).all()