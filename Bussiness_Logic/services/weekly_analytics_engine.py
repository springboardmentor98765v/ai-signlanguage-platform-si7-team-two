"""
Weekly Analytics Engine — Milestone 2, Day 5.

Groups a learner's assessments by calendar week (Mon-Sun) and computes:
- average accuracy for that week
- improvement rate vs the previous week
- weak letters for that week (avg score < WEAK_LETTER_THRESHOLD)

Computed live from existing Assessment data — no new table required today.
If Intern 5 later adds a `weekly_analytics` table for persistence/history,
this function's output maps directly onto it.
"""

from datetime import datetime, timedelta

WEAK_LETTER_THRESHOLD = 70.0


def _week_start(dt: datetime) -> datetime:
    """Returns the Monday 00:00 of the week containing dt."""
    monday = dt - timedelta(days=dt.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def compute_weekly_stats(assessments: list) -> list:
    """
    assessments: list of Assessment rows for one learner (any order).

    Returns a list of weekly summaries, oldest week first:
        {
            "week_start": "2026-07-13",
            "average_accuracy": 78.5,
            "improvement_rate": 12.3,   # None for the very first week
            "weak_letters": ["R", "S"],
            "attempts_count": 14
        }
    """
    weeks = {}
    for a in assessments:
        wk = _week_start(a.created_at)
        weeks.setdefault(wk, []).append(a)

    sorted_weeks = sorted(weeks.keys())

    results = []
    previous_avg = None

    for wk in sorted_weeks:
        week_assessments = weeks[wk]

        avg_accuracy = sum(float(a.overall_score) for a in week_assessments) / len(week_assessments)

        letter_scores = {}
        for a in week_assessments:
            letter_scores.setdefault(a.expected_sign, []).append(float(a.overall_score))

        weak_letters = [
            letter for letter, scores in letter_scores.items()
            if (sum(scores) / len(scores)) < WEAK_LETTER_THRESHOLD
        ]

        improvement_rate = (
            round(avg_accuracy - previous_avg, 2) if previous_avg is not None else None
        )

        results.append({
            "week_start": wk.strftime("%Y-%m-%d"),
            "average_accuracy": round(avg_accuracy, 2),
            "improvement_rate": improvement_rate,
            "weak_letters": sorted(weak_letters),
            "attempts_count": len(week_assessments),
        })

        previous_avg = avg_accuracy

    return results