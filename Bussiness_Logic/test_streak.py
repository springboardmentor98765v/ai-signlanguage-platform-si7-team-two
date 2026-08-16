from datetime import date
from types import SimpleNamespace
from uuid import uuid4

from services.streak_service import update_streak


class FakeQuery:
    def __init__(self, streak):
        self.streak = streak

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.streak


class FakeDB:
    def __init__(self, streak=None):
        self.streak = streak

    def query(self, model):
        return FakeQuery(self.streak)

    def add(self, streak):
        self.streak = streak

    def commit(self):
        pass

    def refresh(self, streak):
        pass


def test_first_practice_creates_streak():
    """First practice should create a streak of 1."""

    learner_id = uuid4()

    db = FakeDB()

    result = update_streak(
        db,
        learner_id,
        date(2026, 8, 1),
    )

    assert result.current_streak == 1
    assert result.longest_streak == 1
    assert result.last_practice_date == date(2026, 8, 1)


def test_next_day_increases_streak():
    """Practicing on the next day should increase the streak."""

    learner_id = uuid4()

    existing_streak = SimpleNamespace(
        learner_id=learner_id,
        current_streak=1,
        longest_streak=1,
        last_practice_date=date(2026, 8, 1),
    )

    db = FakeDB(existing_streak)

    result = update_streak(
        db,
        learner_id,
        date(2026, 8, 2),
    )

    assert result.current_streak == 2
    assert result.longest_streak == 2
    assert result.last_practice_date == date(2026, 8, 2)


def test_same_day_does_not_increase_streak():
    """Practicing again on the same day should not increase the streak."""

    learner_id = uuid4()

    existing_streak = SimpleNamespace(
        learner_id=learner_id,
        current_streak=3,
        longest_streak=3,
        last_practice_date=date(2026, 8, 3),
    )

    db = FakeDB(existing_streak)

    result = update_streak(
        db,
        learner_id,
        date(2026, 8, 3),
    )

    assert result.current_streak == 3
    assert result.longest_streak == 3


def test_missing_day_resets_streak():
    """Missing one or more days should reset the current streak to 1."""

    learner_id = uuid4()

    existing_streak = SimpleNamespace(
        learner_id=learner_id,
        current_streak=5,
        longest_streak=5,
        last_practice_date=date(2026, 8, 1),
    )

    db = FakeDB(existing_streak)

    result = update_streak(
        db,
        learner_id,
        date(2026, 8, 3),
    )

    assert result.current_streak == 1
    assert result.longest_streak == 5
    assert result.last_practice_date == date(2026, 8, 3)


def test_longest_streak_is_preserved():
    """Longest streak should not decrease when the current streak resets."""

    learner_id = uuid4()

    existing_streak = SimpleNamespace(
        learner_id=learner_id,
        current_streak=2,
        longest_streak=7,
        last_practice_date=date(2026, 8, 10),
    )

    db = FakeDB(existing_streak)

    result = update_streak(
        db,
        learner_id,
        date(2026, 8, 12),
    )

    assert result.current_streak == 1
    assert result.longest_streak == 7