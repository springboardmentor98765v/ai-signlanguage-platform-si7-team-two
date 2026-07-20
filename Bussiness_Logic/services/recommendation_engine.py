"""
Recommendation Engine — Milestone 2, Day 4.

Rule: for each letter a learner has attempted, look at their most recent
3 attempts on that letter. If the average overall_score across those
attempts is below RECOMMENDATION_THRESHOLD, flag it as weak.
"""

RECOMMENDATION_THRESHOLD = 70.0
ATTEMPTS_TO_CONSIDER = 3


def find_weak_letters(assessments: list) -> list:
    """
    assessments: list of Assessment rows for this learner.
    Returns a list of dicts: {"letter": ..., "average_score": ...}
    for letters whose most recent 3 attempts average below threshold.
    """
    letter_attempts = {}
    for a in sorted(assessments, key=lambda x: x.created_at, reverse=True):
        letter = a.expected_sign
        if letter:
            letter_attempts.setdefault(letter, []).append(float(a.overall_score))

    weak = []
    for letter, scores in letter_attempts.items():
        recent_scores = scores[:ATTEMPTS_TO_CONSIDER]
        if len(recent_scores) < ATTEMPTS_TO_CONSIDER:
            continue
        avg_recent = sum(recent_scores) / len(recent_scores)
        if avg_recent < RECOMMENDATION_THRESHOLD:
            weak.append({"letter": letter, "average_score": round(avg_recent, 2)})

    weak.sort(key=lambda r: r["average_score"])
    return weak