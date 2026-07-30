from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.analytics_model import AnalyticsSummary
from models.assessment_model import Assessment
from models.practice_model import Lesson, PracticeSession
from schemas.analytics_schema import AnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["Analytics Service"])

WEAK_LETTER_THRESHOLD = 70.0


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}", response_model=AnalyticsResponse)
def get_learner_analytics(user_id: str, db: Session = Depends(get_db)):

    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == user_id)
        .all()
    )

    if not sessions:
        raise HTTPException(
            status_code=404,
            detail="No practice sessions found for this user",
        )

    completed_sessions = [
        s for s in sessions if s.status == "completed"
    ]

    lessons_completed = len(completed_sessions)

    total_practice_time = 0

    for s in completed_sessions:
        if s.start_time and s.end_time:
            total_practice_time += int(
                (s.end_time - s.start_time).total_seconds()
            )

    session_ids = [s.id for s in sessions]

    lesson_ids = [s.lesson_id for s in sessions]

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
        session.id: lesson_letter_map.get(session.lesson_id)
        for session in sessions
    }

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .all()
    )

    if assessments:
        average_accuracy = (
            sum(float(a.overall_score) for a in assessments)
            / len(assessments)
        )
    else:
        average_accuracy = 0.0

    letter_scores = {}

    for assessment in assessments:

        letter = session_letter_map.get(
            assessment.session_id
        )

        if letter:
            letter_scores.setdefault(letter, []).append(
                float(assessment.overall_score)
            )

    weak_letters = []

    for letter, scores in letter_scores.items():

        avg = sum(scores) / len(scores)

        if avg < WEAK_LETTER_THRESHOLD:
            weak_letters.append(letter)

    summary = (
        db.query(AnalyticsSummary)
        .filter(AnalyticsSummary.user_id == user_id)
        .first()
    )

    if not summary:
        summary = AnalyticsSummary(user_id=user_id)
        db.add(summary)

    summary.average_accuracy = round(average_accuracy, 2)
    summary.lessons_completed = lessons_completed
    summary.total_practice_time = total_practice_time
    summary.weak_letters = weak_letters
    summary.last_updated = datetime.utcnow()

    db.commit()
    db.refresh(summary)

    return AnalyticsResponse(
        user_id=summary.user_id,
        average_accuracy=float(summary.average_accuracy),
        lessons_completed=summary.lessons_completed,
        total_practice_time=summary.total_practice_time,
        weak_letters=summary.weak_letters,
        last_updated=summary.last_updated,
    )