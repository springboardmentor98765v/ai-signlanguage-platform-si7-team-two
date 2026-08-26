from services.weekly_analytics_engine import compute_weekly_stats
from datetime import datetime
from types import SimpleNamespace


def make_assessment(letter, score, date_str):
    """date_str: 'YYYY-MM-DD'"""
    return SimpleNamespace(
        expected_sign=letter,
        overall_score=score,
        created_at=datetime.strptime(date_str, "%Y-%m-%d"),
    )


# Week 1 (Mon 2026-08-10 week): 2 assessments
# Week 2 (Mon 2026-08-17 week): 3 assessments
assessments = [
    # Week starting 2026-08-10
    make_assessment("A", 70, "2026-08-10"),
    make_assessment("B", 65, "2026-08-12"),

    # Week starting 2026-08-17
    make_assessment("A", 90, "2026-08-17"),
    make_assessment("R", 60, "2026-08-18"),
    make_assessment("R", 55, "2026-08-19"),
]


def test_weekly_stats_groups_into_correct_weeks():
    result = compute_weekly_stats(assessments)
    print("Weekly stats:")
    for week in result:
        print(" -", week)

    assert len(result) == 2, f"Expected 2 weeks, got {len(result)}: {result}"


def test_weekly_stats_improvement_rate_not_none_after_first_week():
    result = compute_weekly_stats(assessments)
    assert result[-1]["improvement_rate"] is not None


def test_weekly_stats_first_week_has_no_improvement_rate():
    result = compute_weekly_stats(assessments)
    assert result[0]["improvement_rate"] is None


def test_weekly_stats_detects_weak_letters():
    result = compute_weekly_stats(assessments)
    # Week 2: R has avg (60+55)/2 = 57.5 < 70 threshold
    week2 = result[1]
    assert "R" in week2["weak_letters"]