"""
Recommendation Engine — Milestone 2

Find letters whose recent performance is below the threshold.
"""

RECOMMENDATION_THRESHOLD = 70.0
ATTEMPTS_TO_CONSIDER = 3
RECENCY_WEIGHTS = [
    1.0,
    0.7,
    0.4,
]

def find_weak_letters(assessment_session_pairs):

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

        weighted_sum = 0
        total_weight = 0
        for score, weight in zip(recent_scores, RECENCY_WEIGHTS):
            weighted_sum += score * weight
            total_weight += weight
        avg = weighted_sum / total_weight
        
        if avg < RECOMMENDATION_THRESHOLD:
            weak.append(
                {
                    "letter": letter,
                    "average_score": round(avg, 2),
                }
            )

    weak.sort(key=lambda x: x["average_score"])

    return weak