"""
Tests for Milestone 4 Day 3 Trainer Analytics.
"""

from datetime import datetime, date
from types import SimpleNamespace

from services.trainer_analytics_service import (
    calculate_learner_engagement,
    calculate_skill_development,
    calculate_assessment_analytics,
    calculate_certification_status,
    get_trainer_learner_analytics,
)


# =========================================================
# FAKE DATABASE HELPERS
# =========================================================

class FakeQuery:

    def __init__(self, result):
        self.result = result

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return self.result

    def first(self):
        if isinstance(self.result, list):
            return self.result[0] if self.result else None

        return self.result


class FakeDB:

    def __init__(self, query_results):
        self.query_results = iter(query_results)

    def query(self, *args, **kwargs):
        return FakeQuery(next(self.query_results))


# =========================================================
# TEST 1 — LEARNER ENGAGEMENT
# =========================================================

def test_learner_engagement():

    learner_id = "learner-1"

    sessions = [
        SimpleNamespace(
            status="completed",
            attempt_count=3,
            ended_at=datetime(2026, 8, 10, 10, 0),
        ),
        SimpleNamespace(
            status="completed",
            attempt_count=2,
            ended_at=datetime(2026, 8, 11, 10, 0),
        ),
        SimpleNamespace(
            status="in_progress",
            attempt_count=1,
            ended_at=None,
        ),
    ]

    streak = SimpleNamespace(
        current_streak=2,
        longest_streak=5,
    )

    db = FakeDB([
        sessions,
        streak,
    ])

    result = calculate_learner_engagement(
        db,
        learner_id,
    )

    assert result["total_sessions"] == 3
    assert result["completed_sessions"] == 2
    assert result["total_attempts"] == 6
    assert result["current_streak"] == 2
    assert result["longest_streak"] == 5
    assert result["last_practice_date"] == date(2026, 8, 11)


# =========================================================
# TEST 2 — SKILL DEVELOPMENT / IMPROVEMENT
# =========================================================

def test_skill_development_improvement():

    learner_id = "learner-1"

    sessions = [
        SimpleNamespace(id="session-1"),
    ]

    assessments = [
        SimpleNamespace(
            created_at=datetime(2026, 7, 20, 10, 0),
            overall_score=60,
            expected_sign="A",
            session_id="session-1",
        ),
        SimpleNamespace(
            created_at=datetime(2026, 7, 21, 10, 0),
            overall_score=65,
            expected_sign="B",
            session_id="session-1",
        ),
        SimpleNamespace(
            created_at=datetime(2026, 7, 27, 10, 0),
            overall_score=80,
            expected_sign="C",
            session_id="session-1",
        ),
        SimpleNamespace(
            created_at=datetime(2026, 7, 28, 10, 0),
            overall_score=90,
            expected_sign="D",
            session_id="session-1",
        ),
    ]

    db = FakeDB([
        sessions,
        assessments,
    ])

    result = calculate_skill_development(
        db,
        learner_id,
    )

    assert result["current_average"] == 85.0
    assert result["previous_average"] == 62.5
    assert result["improvement_rate"] == 22.5


# =========================================================
# TEST 3 — ASSESSMENT ANALYTICS
# =========================================================

def test_assessment_analytics():

    learner_id = "learner-1"

    sessions = [
        SimpleNamespace(id="session-1"),
    ]

    assessments = [
        SimpleNamespace(overall_score=70),
        SimpleNamespace(overall_score=80),
        SimpleNamespace(overall_score=90),
    ]

    db = FakeDB([
        sessions,
        assessments,
    ])

    result = calculate_assessment_analytics(
        db,
        learner_id,
    )

    assert result["assessment_count"] == 3
    assert result["average_score"] == 80.0
    assert result["highest_score"] == 90.0
    assert result["lowest_score"] == 70.0


# =========================================================
# TEST 4 — NO ASSESSMENTS
# =========================================================

def test_no_assessments():

    learner_id = "learner-1"

    sessions = [
        SimpleNamespace(id="session-1"),
    ]

    db = FakeDB([
        sessions,
        [],
    ])

    result = calculate_assessment_analytics(
        db,
        learner_id,
    )

    assert result["assessment_count"] == 0
    assert result["average_score"] == 0.0
    assert result["highest_score"] == 0.0
    assert result["lowest_score"] == 0.0


# =========================================================
# TEST 5 — CERTIFICATION STATUS
# =========================================================

def test_certification_status():

    learner_id = "learner-1"

    certificate = SimpleNamespace(
        average_score=85.5,
        certificate_code="CERT-001",
        issued_at=datetime(2026, 8, 1),
    )

    db = FakeDB([
        certificate,
    ])

    result = calculate_certification_status(
        db,
        learner_id,
    )

    assert result["status"] == "Certified"
    assert result["eligible"] is True
    assert result["average_score"] == 85.5
    assert result["certificate_code"] == "CERT-001"


# =========================================================
# TEST 6 — NOT CERTIFIED
# =========================================================

def test_not_certified():

    learner_id = "learner-1"

    db = FakeDB([
        None,
    ])

    result = calculate_certification_status(
        db,
        learner_id,
    )

    assert result["status"] == "Not Certified"
    assert result["eligible"] is False
    assert result["average_score"] is None
    assert result["certificate_code"] is None


# =========================================================
# TEST 7 — COMPLETE TRAINER ANALYTICS
# =========================================================

def test_complete_trainer_analytics():

    learner_id = "learner-1"

    sessions = [
        SimpleNamespace(
            id="session-1",
            status="completed",
            attempt_count=2,
            ended_at=datetime(2026, 8, 10, 10, 0),
        ),
    ]

    assessments = [
        SimpleNamespace(
            created_at=datetime(2026, 8, 10, 10, 0),
            overall_score=80,
            expected_sign="A",
            session_id="session-1",
        ),
    ]

    streak = SimpleNamespace(
        current_streak=3,
        longest_streak=5,
    )

    certificate = SimpleNamespace(
        average_score=80.0,
        certificate_code="CERT-001",
        issued_at=datetime(2026, 8, 10),
    )

    db = FakeDB([
        sessions,
        streak,
        sessions,
        assessments,
        sessions,
        assessments,
        certificate,
    ])

    result = get_trainer_learner_analytics(
        db,
        learner_id,
    )

    assert result["learner_id"] == learner_id

    assert result["engagement"]["total_sessions"] == 1

    assert result["engagement"]["completed_sessions"] == 1

    assert result["assessment"]["average_score"] == 80.0

    assert result["certification"]["status"] == "Certified"

    assert result["certification"]["eligible"] is True