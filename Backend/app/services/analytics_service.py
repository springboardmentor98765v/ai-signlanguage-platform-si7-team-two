"""Writes the aggregate learner analytics stored in analytics_summary."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.analytics_summary import AnalyticsSummary


def get_summary_for_learner(db: Session, user_id: UUID) -> AnalyticsSummary | dict:
    """Read persisted summary analytics without creating or mutating a row."""
    summary = db.get(AnalyticsSummary, user_id)
    if summary is not None:
        return summary

    return {
        "average_accuracy": 0.0,
        "lessons_completed": 0,
        "total_practice_time": 0,
        "weak_letters": [],
    }


def update_analytics_summary(
    db: Session,
    user_id: UUID,
    accuracy: float,
    *,
    lesson_completed: bool,
    practice_time: int = 0,
    weak_letters: Optional[Iterable[str]] = None,
) -> AnalyticsSummary:
    """Update the one analytics_summary row for a learner.

    The lesson completion flow supplies ``lesson_completed=True`` only for a
    transition from incomplete to complete. There is no per-attempt aggregate
    history table, so the running average is updated only for that transition;
    retrying an already-completed lesson cannot alter the completed count or
    replace the average with a single latest result.
    """
    summary = db.get(AnalyticsSummary, user_id)
    if summary is None:
        summary = AnalyticsSummary(user_id=user_id)
        db.add(summary)
        db.flush()

    if lesson_completed:
        previous_count = summary.lessons_completed
        accuracy_value = Decimal(str(accuracy))
        previous_total = Decimal(summary.average_accuracy or 0) * previous_count
        summary.lessons_completed = previous_count + 1
        summary.average_accuracy = (
            (previous_total + accuracy_value) / summary.lessons_completed
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if practice_time > 0:
        summary.total_practice_time = (summary.total_practice_time or 0) + practice_time

    if weak_letters is not None:
        summary.weak_letters = list(weak_letters)

    summary.last_updated = datetime.now(timezone.utc)
    return summary
