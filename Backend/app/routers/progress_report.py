from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
import requests

from sqlalchemy.orm import Session

from app.core.security import require_learner
from app.database.database import get_db
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress
from app.models.user import User
from app.schemas.analytics_schema import AnalyticsSummaryResponse
from app.services.analytics_service import get_summary_for_learner
from app.services.integration_service import IntegrationService

router = APIRouter()


def get_local_progress_report(user_id: UUID, db: Session) -> dict:
    """Build the report from Backend-owned learner progress and analytics.

    The business-logic service owns detailed practice-session reports.  Lesson
    completion and analytics are stored by this service, however, so learners
    with that data must still receive a report when they have no corresponding
    business-logic practice-session rows.
    """
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    summary = get_summary_for_learner(db, user_id)
    completed_lessons = (
        db.query(Lesson.letter)
        .join(LessonProgress, LessonProgress.lesson_id == Lesson.id)
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.is_completed.is_(True),
        )
        .order_by(Lesson.order_index)
        .all()
    )
    attempted_letters = list(dict.fromkeys(letter for (letter,) in completed_lessons))

    def summary_value(name: str, default):
        return getattr(summary, name, default) if not isinstance(summary, dict) else summary.get(name, default)

    return {
        "user_id": user_id,
        "full_name": user.full_name,
        "lessons_completed": summary_value("lessons_completed", len(attempted_letters)),
        "total_practice_time": summary_value("total_practice_time", 0),
        "average_accuracy": summary_value("average_accuracy", 0),
        "attempted_letters": attempted_letters,
        "weak_letters": summary_value("weak_letters", []) or [],
        # The Backend schema does not retain an attempt-level aggregate.
        "total_attempts": 0,
        "certificates_earned": [],
        "generated_at": datetime.now(timezone.utc),
    }


@router.get("/{user_id}/summary", response_model=AnalyticsSummaryResponse)
def get_persisted_summary(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_learner),
):
    """Return the authenticated learner's persisted analytics_summary row."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own analytics summary",
        )

    return get_summary_for_learner(db, user_id)


@router.get("/{user_id}")
def get_progress_report(user_id: UUID, db: Session = Depends(get_db)):
    try:
        return IntegrationService.get_progress_report(str(user_id))

    except requests.exceptions.HTTPError as e:
        # A 404 here comes from the business-logic service when it has no
        # PracticeSession rows. It is not a missing route: use the learner's
        # Backend-owned lesson progress and analytics instead.
        if e.response is not None and e.response.status_code == status.HTTP_404_NOT_FOUND:
            return get_local_progress_report(user_id, db)

        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text

        raise HTTPException(
            status_code=e.response.status_code,
            detail=detail,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/{user_id}/download")
def download_progress_report(
    user_id: str,
    learner_name: str,
):

    try:
        pdf = IntegrationService.download_progress_report(
            user_id,
            learner_name,
        )

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f'attachment; filename="Progress_Report_{learner_name}.pdf"'
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
