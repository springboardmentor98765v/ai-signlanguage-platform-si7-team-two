"""
Certificate Eligibility Engine — Milestone 2, Day 6.

Rule: a learner is eligible for a certificate when they have attempted
every letter in the seeded lesson catalogue at least once, AND their
overall average score across all attempts is >= CERTIFICATE_THRESHOLD.
"""

import uuid

CERTIFICATE_THRESHOLD = 80.0


def check_certificate_eligibility(assessments: list, required_letters: list) -> dict:
    """
    assessments: list of Assessment rows for this learner.
    required_letters: list of every letter in the seeded lesson catalogue
                       (e.g. from Lesson.letter across all lessons).

    Returns:
        {
            "eligible": bool,
            "average_score": float,
            "attempted_letters": ["A", "B", ...],
            "missing_letters": ["Z"],   # empty if eligible
            "attempts_count": int
        }
    """
    if not assessments:
        return {
            "eligible": False,
            "average_score": 0.0,
            "attempted_letters": [],
            "missing_letters": sorted(set(required_letters)),
            "attempts_count": 0,
        }

    attempted_letters = {a.expected_sign for a in assessments}
    required_set = set(required_letters)
    missing_letters = sorted(required_set - attempted_letters)

    average_score = sum(float(a.overall_score) for a in assessments) / len(assessments)

    eligible = (len(missing_letters) == 0) and (average_score >= CERTIFICATE_THRESHOLD)

    return {
        "eligible": eligible,
        "average_score": round(average_score, 2),
        "attempted_letters": sorted(attempted_letters),
        "missing_letters": missing_letters,
        "attempts_count": len(assessments),
    }


def generate_certificate_code(learner_id) -> str:
    """Short, unique, human-shareable code for certificate verification."""
    return f"CERT-{str(learner_id)[:8].upper()}-{uuid.uuid4().hex[:6].upper()}"