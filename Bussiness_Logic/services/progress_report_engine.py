"""
Progress Report Engine — Day 8.
Combines a learner's session history, assessment history, and
certificate records into one full-journey summary.
"""

def build_progress_report(sessions: list, assessments: list, certificates: list) -> dict:
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

    letter_scores = {}
    for a in assessments:
        letter = getattr(a, "expected_sign", None)
        if letter:
            letter_scores.setdefault(letter, []).append(float(a.overall_score))

    attempted_letters = sorted(letter_scores.keys())
    weak_letters = [
        letter for letter, scores in letter_scores.items()
        if (sum(scores) / len(scores)) < 70.0
    ]

    certificates_summary = [
        {
            "certificate_code": c.certificate_code,
            "average_score": float(c.average_score),
            "issued_at": c.issued_at if hasattr(c, "issued_at") else None
        }
        for c in certificates
    ]

    return {
        "lessons_completed": lessons_completed,
        "total_practice_time": total_practice_time,
        "average_accuracy": round(average_accuracy, 2),
        "attempted_letters": attempted_letters,
        "weak_letters": sorted(weak_letters),
        "total_attempts": len(assessments),
        "certificates_earned": certificates_summary
    }