from services.recommendation_engine import find_weak_letters
from datetime import datetime, timedelta
from types import SimpleNamespace

def make_assessment(letter, score, minutes_ago):
    return SimpleNamespace(
        expected_sign=letter,
        overall_score=score,
        created_at=datetime.utcnow() - timedelta(minutes=minutes_ago),
    )

assessments = [
    make_assessment("R", 60, minutes_ago=1),
    make_assessment("R", 55, minutes_ago=5),
    make_assessment("R", 65, minutes_ago=10),
    make_assessment("R", 90, minutes_ago=20),

    make_assessment("A", 95, minutes_ago=1),
    make_assessment("A", 92, minutes_ago=5),
    make_assessment("A", 98, minutes_ago=10),
]

result = find_weak_letters(assessments)
print("Weak letters found:", result)

assert len(result) == 1
assert result[0]["letter"] == "R"
print("\nTest passed!")