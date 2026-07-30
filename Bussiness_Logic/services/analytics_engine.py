"""
Analytics aggregation logic for Milestone 1.
Computes summary stats for a learner from their practice_sessions
and assessments history.
"""

WEAK_LETTER_THRESHOLD = 70.0

def compute_learner_stats(sessions: list, assessments: list) -> dict:
    """
    sessions: list of PracticeSession rows for this user
    assessments: list of Assessment rows linked to those sessions
    """
    completed_sessions = [s for s in sessions if s.status == "completed"]
    lessons_completed = len(completed_sessions)

    total_practice_time = 0
    for s in completed_sessions:
        if s.ended_at and s.started_at:
            total_practice_time += int((s.ended_at - s.started_at).total_seconds())
    if assessments:
        average_accuracy = sum(float(a.overall_score) for a in assessments) / len(assessments)
    else:
        average_accuracy = 0.0

    # Track average score per letter to find weak ones
    letter_scores = {}
    for a in assessments:
        letter = a.expected_sign if hasattr(a, "expected_sign") else None
        # fallback: use predicted_sign's session's expected_sign via session map (handled in router)
        if letter:
            letter_scores.setdefault(letter, []).append(float(a.overall_score))

    weak_letters = [
        letter for letter, scores in letter_scores.items()
        if (sum(scores) / len(scores)) < WEAK_LETTER_THRESHOLD
    ]

    return {
        "average_accuracy": round(average_accuracy, 2),
        "lessons_completed": lessons_completed,
        "total_practice_time": total_practice_time,
        "weak_letters": weak_letters
    }