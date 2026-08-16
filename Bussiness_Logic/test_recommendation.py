from services.recommendation_engine import find_weak_letters
from datetime import datetime, timedelta
from types import SimpleNamespace


def make_pair(letter, score, minutes_ago):
    assessment = SimpleNamespace(
        overall_score=score,
        created_at=datetime.utcnow() - timedelta(minutes=minutes_ago),
    )

    session = SimpleNamespace(
        expected_sign=letter,
    )

    return assessment, session


def test_finds_weak_letter():
    """R should be recommended because its recent weighted score is below 70."""

    assessments = [
        make_pair("R", 60, 1),
        make_pair("R", 55, 5),
        make_pair("R", 65, 10),
        make_pair("R", 90, 20),

        make_pair("A", 95, 1),
        make_pair("A", 92, 5),
        make_pair("A", 98, 10),
    ]

    result = find_weak_letters(assessments)

    assert len(result) == 1
    assert result[0]["letter"] == "R"


def test_strong_letter_is_not_recommended():
    """A strong recent performance should not be recommended."""

    assessments = [
        make_pair("A", 95, 1),
        make_pair("A", 92, 5),
        make_pair("A", 98, 10),
    ]

    result = find_weak_letters(assessments)

    assert result == []


def test_letter_with_fewer_than_three_attempts_is_ignored():
    """Recommendation requires at least three attempts."""

    assessments = [
        make_pair("R", 40, 1),
        make_pair("R", 50, 5),
    ]

    result = find_weak_letters(assessments)

    assert result == []


def test_weighted_recent_scores_are_used():
    """Recent attempts have greater weight than older attempts."""

    assessments = [
        make_pair("R", 50, 1),
        make_pair("R", 50, 5),
        make_pair("R", 90, 10),
    ]

    result = find_weak_letters(assessments)

    assert len(result) == 1
    assert result[0]["letter"] == "R"
    assert result[0]["average_score"] < 70