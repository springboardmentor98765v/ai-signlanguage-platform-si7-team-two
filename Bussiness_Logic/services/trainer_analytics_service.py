"""
Accessibility Trainer Analytics Service — Milestone 4, Day 3.

Provides business-logic calculations for the Accessibility Trainer Dashboard:

1. Learner engagement
2. Skill development / improvement
3. Assessment analytics
4. Certification status

Intern 2 can expose these calculations through Trainer Dashboard APIs.
"""

from typing import Any

from sqlalchemy.orm import Session

from models.practice_model import PracticeSession, Certificate
from models.assessment_model import Assessment
from models.streak_model import Streak

from services.weekly_analytics_engine import compute_weekly_stats


# =========================================================
# 1. LEARNER ENGAGEMENT
# =========================================================

def calculate_learner_engagement(
    db: Session,
    learner_id,
) -> dict[str, Any]:
    """
    Calculates how actively a learner practices.

    Uses:
    - practice_sessions
    - streaks
    """

    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == learner_id)
        .all()
    )

    total_sessions = len(sessions)

    completed_sessions = [
        session
        for session in sessions
        if session.status == "completed"
    ]

    completed_session_count = len(completed_sessions)

    total_attempts = sum(
        session.attempt_count or 0
        for session in sessions
    )

    last_practice_date = None

    practice_dates = [
        session.ended_at.date()
        for session in completed_sessions
        if session.ended_at is not None
    ]

    if practice_dates:
        last_practice_date = max(practice_dates)

    streak = (
        db.query(Streak)
        .filter(Streak.learner_id == learner_id)
        .first()
    )

    current_streak = 0
    longest_streak = 0

    if streak:
        current_streak = streak.current_streak
        longest_streak = streak.longest_streak

    return {
        "total_sessions": total_sessions,
        "completed_sessions": completed_session_count,
        "total_attempts": total_attempts,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_practice_date": last_practice_date,
    }


# =========================================================
# 2. SKILL DEVELOPMENT / IMPROVEMENT
# =========================================================

def calculate_skill_development(
    db: Session,
    learner_id,
) -> dict[str, Any]:
    """
    Calculates learner improvement over time.

    Reuses the existing weekly analytics engine instead
    of creating a second improvement formula.
    """

    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == learner_id)
        .all()
    )

    session_ids = [session.id for session in sessions]

    if not session_ids:
        return {
            "current_average": 0.0,
            "previous_average": 0.0,
            "improvement_rate": 0.0,
        }

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .order_by(Assessment.created_at.asc())
        .all()
    )

    if not assessments:
        return {
            "current_average": 0.0,
            "previous_average": 0.0,
            "improvement_rate": 0.0,
        }

    weekly_stats = compute_weekly_stats(assessments)

    if not weekly_stats:
        return {
            "current_average": 0.0,
            "previous_average": 0.0,
            "improvement_rate": 0.0,
        }

    current_average = weekly_stats[-1]["average_accuracy"]

    if len(weekly_stats) >= 2:
        previous_average = weekly_stats[-2]["average_accuracy"]
        improvement_rate = round(
            current_average - previous_average,
            2,
        )
    else:
        previous_average = 0.0
        improvement_rate = 0.0

    return {
        "current_average": current_average,
        "previous_average": previous_average,
        "improvement_rate": improvement_rate,
    }


# =========================================================
# 3. ASSESSMENT ANALYTICS
# =========================================================

def calculate_assessment_analytics(
    db: Session,
    learner_id,
) -> dict[str, Any]:
    """
    Calculates assessment performance.

    Uses Assessment.overall_score, which is the final
    score produced by the existing weighted scoring engine.
    """

    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == learner_id)
        .all()
    )

    session_ids = [session.id for session in sessions]

    if not session_ids:
        return {
            "assessment_count": 0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
        }

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .all()
    )

    scores = [
        float(assessment.overall_score)
        for assessment in assessments
        if assessment.overall_score is not None
    ]

    if not scores:
        return {
            "assessment_count": 0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
        }

    return {
        "assessment_count": len(scores),
        "average_score": round(
            sum(scores) / len(scores),
            2,
        ),
        "highest_score": round(max(scores), 2),
        "lowest_score": round(min(scores), 2),
    }


# =========================================================
# 4. CERTIFICATION STATUS
# =========================================================

def calculate_certification_status(
    db: Session,
    learner_id,
) -> dict[str, Any]:
    """
    Calculates certification status from existing certificates.

    A valid certificate means the learner has already earned
    a certificate.

    If no certificate exists, the learner is not certified.
    """

    certificate = (
        db.query(Certificate)
        .filter(
            Certificate.learner_id == learner_id,
            Certificate.is_valid.is_(True),
        )
        .order_by(Certificate.issued_at.desc())
        .first()
    )

    if certificate:
        return {
            "status": "Certified",
            "eligible": True,
            "average_score": float(
                certificate.average_score
            ),
            "certificate_code": certificate.certificate_code,
            "issued_at": certificate.issued_at,
        }

    return {
        "status": "Not Certified",
        "eligible": False,
        "average_score": None,
        "certificate_code": None,
        "issued_at": None,
    }


# =========================================================
# 5. COMPLETE TRAINER ANALYTICS
# =========================================================

def get_trainer_learner_analytics(
    db: Session,
    learner_id,
) -> dict[str, Any]:
    """
    Returns all Accessibility Trainer Dashboard
    calculations for one learner.
    """

    engagement = calculate_learner_engagement(
        db,
        learner_id,
    )

    skill_development = calculate_skill_development(
        db,
        learner_id,
    )

    assessment = calculate_assessment_analytics(
        db,
        learner_id,
    )

    certification = calculate_certification_status(
        db,
        learner_id,
    )

    return {
        "learner_id": str(learner_id),
        "engagement": engagement,
        "skill_development": skill_development,
        "assessment": assessment,
        "certification": certification,
    }