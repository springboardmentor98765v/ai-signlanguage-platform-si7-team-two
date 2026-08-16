from types import SimpleNamespace
from uuid import uuid4

from services.badge_service import (
    check_first_steps,
    check_alphabet_master,
)


def test_first_steps_badge_is_earned():
    """First Steps requires at least one completed session."""

    user_id = uuid4()

    session = SimpleNamespace(
        user_id=user_id,
        status="completed",
    )

    class FakeQuery:
        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return [session]

    class FakeDB:
        def query(self, model):
            return FakeQuery()

    db = FakeDB()

    result = check_first_steps(db, user_id)

    assert result is True


def test_first_steps_not_earned_without_completed_session():
    """First Steps should not be earned without completed practice."""

    user_id = uuid4()

    session = SimpleNamespace(
        user_id=user_id,
        status="in_progress",
    )

    class FakeQuery:
        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return [session]

    class FakeDB:
        def query(self, model):
            return FakeQuery()

    db = FakeDB()

    result = check_first_steps(db, user_id)

    assert result is False


def test_alphabet_master_requires_all_26_letters():
    """Alphabet Master requires all 26 letters."""

    user_id = uuid4()

    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    rows = [
        (
            SimpleNamespace(overall_score=90.0),
            letter,
        )
        for letter in letters
    ]

    class FakeQuery:
        def join(self, *args, **kwargs):
            return self

        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return rows

    class FakeDB:
        def query(self, *models):
            return FakeQuery()

    db = FakeDB()

    result = check_alphabet_master(db, user_id)

    assert result is True


def test_alphabet_master_fails_when_letter_missing():
    """Alphabet Master should fail if even one letter is missing."""

    user_id = uuid4()

    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXY")

    rows = [
        (
            SimpleNamespace(overall_score=90.0),
            letter,
        )
        for letter in letters
    ]

    class FakeQuery:
        def join(self, *args, **kwargs):
            return self

        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return rows

    class FakeDB:
        def query(self, *models):
            return FakeQuery()

    db = FakeDB()

    result = check_alphabet_master(db, user_id)

    assert result is False


def test_alphabet_master_fails_below_80_average():
    """Alphabet Master requires average score of at least 80."""

    user_id = uuid4()

    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    rows = [
        (
            SimpleNamespace(overall_score=70.0),
            letter,
        )
        for letter in letters
    ]

    class FakeQuery:
        def join(self, *args, **kwargs):
            return self

        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return rows

    class FakeDB:
        def query(self, *models):
            return FakeQuery()

    db = FakeDB()

    result = check_alphabet_master(db, user_id)

    assert result is False