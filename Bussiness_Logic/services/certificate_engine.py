"""
Certificate Eligibility Engine — Milestone 2, Day 6.

A learner is eligible for a certificate when:
1. They have attempted every required letter at least once.
2. Their average assessment score is >= CERTIFICATE_THRESHOLD.
"""

import uuid

CERTIFICATE_THRESHOLD = 80.0


def check_certificate_eligibility(
    sessions: list,
    assessments: list,
    required_letters: list,
) -> dict:
    """
    sessions: PracticeSession rows
    assessments: Assessment rows
    required_letters: All lesson letters
    """

    if not assessments:
        return {
            "eligible": False,
            "average_score": 0.0,
            "attempted_letters": [],
            "missing_letters": sorted(set(required_letters)),
            "attempts_count": 0,
        }

    # Letters attempted come from PracticeSession
    attempted_letters = {
        session.expected_sign
        for session in sessions
        if session.expected_sign
    }

    required_set = set(required_letters)
    missing_letters = sorted(required_set - attempted_letters)

    average_score = (
        sum(float(a.overall_score) for a in assessments)
        / len(assessments)
    )

    eligible = (
        len(missing_letters) == 0
        and average_score >= CERTIFICATE_THRESHOLD
    )

    return {
        "eligible": eligible,
        "average_score": round(average_score, 2),
        "attempted_letters": sorted(attempted_letters),
        "missing_letters": missing_letters,
        "attempts_count": len(assessments),
    }


def generate_certificate_code(learner_id) -> str:
    return (
        f"CERT-{str(learner_id)[:8].upper()}-"
        f"{uuid.uuid4().hex[:6].upper()}"
    )