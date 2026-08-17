"""
Learner Analytics Service

Calculates and stores learner analytics from:
- practice_sessions
- assessments
- lessons

This service is reusable by:
1. GET /analytics/{user_id}
2. POST /practice/end

This keeps learner_analytics automatically up to date.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from models.analytics_model import AnalyticsSummary
from models.assessment_model import Assessment
from models.practice_model import Lesson, PracticeSession


WEAK_LETTER_THRESHOLD = 70.0


def refresh_learner_analytics(
    db: Session,
    user_id: UUID,
) -> AnalyticsSummary:
    """
    Calculate the latest analytics for a learner and
    create/update their learner_analytics row.

    Returns the AnalyticsSummary database row.
    """

    # ---------------------------------------------------------
    # 1. Get practice sessions
    # ---------------------------------------------------------

    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == user_id)
        .all()
    )

    completed_sessions = [
        session
        for session in sessions
        if session.status == "completed"
    ]

    lessons_completed = len(completed_sessions)

    # ---------------------------------------------------------
    # 2. Calculate total practice time
    # ---------------------------------------------------------

    total_practice_time = 0

    for session in completed_sessions:
        if session.started_at and session.ended_at:
            total_practice_time += int(
                (
                    session.ended_at - session.started_at
                ).total_seconds()
            )

    # ---------------------------------------------------------
    # 3. Get assessments
    # ---------------------------------------------------------

    session_ids = [session.id for session in sessions]

    assessments = []

    if session_ids:
        assessments = (
            db.query(Assessment)
            .filter(
                Assessment.session_id.in_(session_ids)
            )
            .all()
        )

    # ---------------------------------------------------------
    # 4. Calculate average accuracy
    # ---------------------------------------------------------

    if assessments:
        average_accuracy = (
            sum(
                float(assessment.overall_score)
                for assessment in assessments
            )
            / len(assessments)
        )
    else:
        average_accuracy = 0.0

    # ---------------------------------------------------------
    # 5. Map session -> lesson -> letter
    # ---------------------------------------------------------

    lesson_ids = [
        session.lesson_id
        for session in sessions
        if session.lesson_id is not None
    ]

    lessons = []

    if lesson_ids:
        lessons = (
            db.query(Lesson)
            .filter(Lesson.id.in_(lesson_ids))
            .all()
        )

    lesson_letter_map = {
        lesson.id: lesson.letter
        for lesson in lessons
    }

    session_letter_map = {
        session.id: lesson_letter_map.get(
            session.lesson_id
        )
        for session in sessions
    }

    # ---------------------------------------------------------
    # 6. Calculate weak letters
    # ---------------------------------------------------------

    letter_scores = {}

    for assessment in assessments:

        letter = session_letter_map.get(
            assessment.session_id
        )

        if letter:
            letter_scores.setdefault(
                letter,
                [],
            ).append(
                float(assessment.overall_score)
            )

    weak_letters = []

    for letter, scores in letter_scores.items():

        average_score = (
            sum(scores) / len(scores)
        )

        if average_score < WEAK_LETTER_THRESHOLD:
            weak_letters.append(letter)

    weak_letters.sort()

    # ---------------------------------------------------------
    # 7. Create or update learner_analytics row
    # ---------------------------------------------------------

    summary = (
        db.query(AnalyticsSummary)
        .filter(
            AnalyticsSummary.user_id == user_id
        )
        .first()
    )

    if summary is None:

        summary = AnalyticsSummary(
            user_id=user_id,
        )

        db.add(summary)

    summary.average_accuracy = round(
        average_accuracy,
        2,
    )

    summary.lessons_completed = lessons_completed

    summary.total_practice_time = total_practice_time

    summary.weak_letters = weak_letters

    summary.last_updated = datetime.utcnow()

    # ---------------------------------------------------------
    # 8. Save changes
    # ---------------------------------------------------------

    db.commit()
    db.refresh(summary)

    return summary