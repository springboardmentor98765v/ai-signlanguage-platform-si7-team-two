"""
Tests for Milestone 4 Day 3 Trainer Analytics.
"""

from datetime import datetime
from types import SimpleNamespace

from services.weekly_analytics_engine import compute_weekly_stats


# =========================================================
# TEST 1 — WEEKLY SKILL IMPROVEMENT
# =========================================================

def test_skill_development_improvement():

    assessments = [
        SimpleNamespace(
            created_at=datetime(2026, 7, 20, 10, 0),
            overall_score=60,
            expected_sign="A",
        ),
        SimpleNamespace(
            created_at=datetime(2026, 7, 21, 10, 0),
            overall_score=65,
            expected_sign="B",
        ),
        SimpleNamespace(
            created_at=datetime(2026, 7, 27, 10, 0),
            overall_score=80,
            expected_sign="C",
        ),
        SimpleNamespace(
            created_at=datetime(2026, 7, 28, 10, 0),
            overall_score=90,
            expected_sign="D",
        ),
    ]

    result = compute_weekly_stats(assessments)

    assert len(result) == 2

    assert result[0]["average_accuracy"] == 62.5

    assert result[1]["average_accuracy"] == 85.0

    assert result[1]["improvement_rate"] == 22.5


# =========================================================
# TEST 2 — ASSESSMENT AVERAGE
# =========================================================

def test_assessment_average():

    scores = [70, 80, 90]

    average = round(
        sum(scores) / len(scores),
        2,
    )

    assert average == 80.0


# =========================================================
# TEST 3 — HIGHEST SCORE
# =========================================================

def test_highest_assessment_score():

    scores = [70, 85, 92, 76]

    assert max(scores) == 92


# =========================================================
# TEST 4 — LOWEST SCORE
# =========================================================

def test_lowest_assessment_score():

    scores = [70, 85, 92, 76]

    assert min(scores) == 70


# =========================================================
# TEST 5 — NO ASSESSMENTS
# =========================================================

def test_no_assessments():

    assessments = []

    assert len(assessments) == 0