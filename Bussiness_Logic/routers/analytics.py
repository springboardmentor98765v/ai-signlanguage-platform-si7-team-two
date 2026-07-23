from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession, Lesson
from models.assessment_model import Assessment
from models.analytics_model import AnalyticsSummary
from schemas.analytics_schema import AnalyticsResponse
from datetime import datetime

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
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == user_id).all()
    if not sessions:
        raise HTTPException(status_code=404, detail="No practice sessions found for this user")

    completed_sessions = [s for s in sessions if s.status == "completed"]
    lessons_completed = len(completed_sessions)

    total_practice_time = 0
    for s in completed_sessions:
        if s.ended_at and s.started_at:
            total_practice_time += int((s.ended_at - s.started_at).total_seconds())

    session_ids = [s.id for s in sessions]

    # Build session_id -> letter map by joining each session's lesson
    lesson_ids = [s.lesson_id for s in sessions]
    lessons = db.query(Lesson).filter(Lesson.id.in_(lesson_ids)).all()
    lesson_letter_map = {l.id: l.letter for l in lessons}
    session_letter_map = {s.id: lesson_letter_map.get(s.lesson_id) for s in sessions}

    assessments = db.query(Assessment).filter(Assessment.session_id.in_(session_ids)).all()

    if assessments:
        average_accuracy = sum(float(a.overall_score) for a in assessments) / len(assessments)
    else:
        average_accuracy = 0.0

    letter_scores = {}
    for a in assessments:
        letter = session_letter_map.get(a.session_id)
        if letter:
            letter_scores.setdefault(letter, []).append(float(a.overall_score))

    weak_letters = [
        letter for letter, scores in letter_scores.items()
        if (sum(scores) / len(scores)) < WEAK_LETTER_THRESHOLD
    ]

    summary = db.query(AnalyticsSummary).filter(AnalyticsSummary.user_id == user_id).first()
    if not summary:
        summary = AnalyticsSummary(user_id=user_id)
        db.add(summary)

    summary.average_accuracy = round(average_accuracy, 2)
    summary.lessons_completed = lessons_completed
    summary.weak_letters = weak_letters
    summary.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(summary)

    return AnalyticsResponse(
        user_id=summary.user_id,
        average_accuracy=float(summary.average_accuracy),
        lessons_completed=summary.lessons_completed,
        total_practice_time=total_practice_time,
        weak_letters=summary.weak_letters,
        last_updated=summary.updated_at
    )