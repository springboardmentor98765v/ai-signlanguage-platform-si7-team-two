from services.weekly_analytics_engine import compute_weekly_stats
from datetime import datetime, timedelta
from types import SimpleNamespace

def make_assessment(letter, score, days_ago):
    return SimpleNamespace(
        expected_sign=letter,
        overall_score=score,
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    )

assessments = [
    # This week: doing well overall, but weak on "R"
    make_assessment("A", 90, days_ago=1),
    make_assessment("R", 60, days_ago=2),
    make_assessment("R", 55, days_ago=3),

    # Last week: lower average overall
    make_assessment("A", 70, days_ago=9),
    make_assessment("B", 65, days_ago=10),
]

result = compute_weekly_stats(assessments)
print("Weekly stats:")
for week in result:
    print(" -", week)

assert len(result) == 2
assert result[-1]["improvement_rate"] is not None
print("\nTest passed!")