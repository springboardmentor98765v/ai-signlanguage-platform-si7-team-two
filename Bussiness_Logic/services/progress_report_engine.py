"""
Progress Report Engine — Day 8.
Combines a learner's session history, assessment history,
and certificate records into one complete learner report.
"""


def build_progress_report(
    sessions: list,
    assessments: list,
    certificates: list,
) -> dict:

    completed_sessions = [
        s for s in sessions
        if s.status == "completed"
    ]

    lessons_completed = len(completed_sessions)

    # Total practice time
    total_practice_time = 0

    for session in completed_sessions:
        if session.started_at and session.ended_at:
            total_practice_time += int(
                (session.ended_at - session.started_at).total_seconds()
            )

    # Average accuracy
    if assessments:
        average_accuracy = (
            sum(float(a.overall_score) for a in assessments)
            / len(assessments)
        )
    else:
        average_accuracy = 0.0

    # Map session_id -> expected letter
    session_letter_map = {
        session.id: session.expected_sign
        for session in sessions
        if session.expected_sign
    }

    # Build per-letter scores
    letter_scores = {}

    for assessment in assessments:

        letter = session_letter_map.get(
            assessment.session_id
        )

        if letter:
            letter_scores.setdefault(letter, []).append(
                float(assessment.overall_score)
            )

    attempted_letters = sorted(letter_scores.keys())

    weak_letters = [
        letter
        for letter, scores in letter_scores.items()
        if (sum(scores) / len(scores)) < 70.0
    ]

    certificates_summary = [
        {
            "certificate_code": cert.certificate_code,
            "average_score": float(cert.average_score),
            "issued_at": getattr(cert, "issued_at", None),
        }
        for cert in certificates
    ]

    return {
        "lessons_completed": lessons_completed,
        "total_practice_time": total_practice_time,
        "average_accuracy": round(average_accuracy, 2),
        "attempted_letters": attempted_letters,
        "weak_letters": sorted(weak_letters),
        "total_attempts": len(assessments),
        "certificates_earned": certificates_summary,
    }