"""
Recommendation Engine — Milestone 2

Find letters whose recent performance is below the threshold.
"""

RECOMMENDATION_THRESHOLD = 70.0
ATTEMPTS_TO_CONSIDER = 3


def find_weak_letters(assessment_session_pairs):
    """
    assessment_session_pairs:
        List of tuples:
        (
            Assessment,
            PracticeSession
        )

    Returns:
        [
            {
                "letter": "A",
                "average_score": 65.2
            }
        ]
    """

    letter_attempts = {}

    sorted_pairs = sorted(
        assessment_session_pairs,
        key=lambda x: x[0].created_at,
        reverse=True,
    )

    for assessment, session in sorted_pairs:

        letter = session.expected_sign

        if not letter:
            continue

        letter_attempts.setdefault(letter, []).append(
            float(assessment.overall_score)
        )

    weak = []

    for letter, scores in letter_attempts.items():

        recent_scores = scores[:ATTEMPTS_TO_CONSIDER]

        if len(recent_scores) < ATTEMPTS_TO_CONSIDER:
            continue

        avg = sum(recent_scores) / len(recent_scores)

        if avg < RECOMMENDATION_THRESHOLD:
            weak.append(
                {
                    "letter": letter,
                    "average_score": round(avg, 2),
                }
            )

    weak.sort(key=lambda x: x["average_score"])

    return weak