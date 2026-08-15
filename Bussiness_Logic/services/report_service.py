"""
Report Service — Milestone 4, Day 4.

Builds data for the four additional report types:
1. Learning Report
2. Assessment Report
3. Accuracy Report
4. Certification Report

The existing Progress Report remains unchanged.
"""

from collections import defaultdict


# ---------------------------------------------------------
# 1. LEARNING REPORT
# ---------------------------------------------------------

def build_learning_report(
    sessions: list,
    assessments: list,
) -> dict:
    """
    Builds learning/practice summary for a learner.
    """

    completed_sessions = [
        session
        for session in sessions
        if session.status == "completed"
    ]

    total_practice_time = 0

    for session in completed_sessions:
        if session.started_at and session.ended_at:
            total_practice_time += int(
                (session.ended_at - session.started_at).total_seconds()
            )

    attempted_letters = sorted({
        session.expected_sign
        for session in sessions
        if session.expected_sign
    })

    return {
        "total_sessions": len(sessions),
        "completed_sessions": len(completed_sessions),
        "total_practice_time": total_practice_time,
        "attempted_letters": attempted_letters,
        "total_assessments": len(assessments),
    }


# ---------------------------------------------------------
# 2. ASSESSMENT REPORT
# ---------------------------------------------------------

def build_assessment_report(
    assessments: list,
) -> dict:
    """
    Builds assessment performance summary.
    """

    if not assessments:
        return {
            "total_assessments": 0,
            "average_score": 0.0,
            "correct_assessments": 0,
            "incorrect_assessments": 0,
            "assessment_scores": [],
        }

    scores = [
        float(assessment.overall_score)
        for assessment in assessments
    ]

    correct_count = sum(
        1
        for assessment in assessments
        if assessment.is_correct
    )

    incorrect_count = len(assessments) - correct_count

    return {
        "total_assessments": len(assessments),
        "average_score": round(
            sum(scores) / len(scores),
            2,
        ),
        "correct_assessments": correct_count,
        "incorrect_assessments": incorrect_count,
        "assessment_scores": [
            {
                "expected_sign": assessment.expected_sign,
                "predicted_sign": assessment.predicted_sign,
                "score": float(assessment.overall_score),
                "is_correct": assessment.is_correct,
            }
            for assessment in assessments
        ],
    }


# ---------------------------------------------------------
# 3. ACCURACY REPORT
# ---------------------------------------------------------

def build_accuracy_report(
    assessments: list,
) -> dict:
    """
    Builds accuracy statistics overall and by letter.
    """

    if not assessments:
        return {
            "overall_accuracy": 0.0,
            "strong_letters": [],
            "weak_letters": [],
            "letter_accuracy": {},
        }

    overall_accuracy = (
        sum(float(a.overall_score) for a in assessments)
        / len(assessments)
    )

    letter_scores = defaultdict(list)

    for assessment in assessments:
        letter_scores[
            assessment.expected_sign
        ].append(
            float(assessment.overall_score)
        )

    letter_accuracy = {
        letter: round(
            sum(scores) / len(scores),
            2,
        )
        for letter, scores in letter_scores.items()
    }

    strong_letters = sorted([
        letter
        for letter, score in letter_accuracy.items()
        if score >= 80.0
    ])

    weak_letters = sorted([
        letter
        for letter, score in letter_accuracy.items()
        if score < 70.0
    ])

    return {
        "overall_accuracy": round(
            overall_accuracy,
            2,
        ),
        "letter_accuracy": letter_accuracy,
        "strong_letters": strong_letters,
        "weak_letters": weak_letters,
    }


# ---------------------------------------------------------
# 4. CERTIFICATION REPORT
# ---------------------------------------------------------

def build_certification_report(
    certificates: list,
) -> dict:
    """
    Builds certification status and certificate history.
    """

    certificate_data = []

    for certificate in certificates:
        certificate_data.append({
            "certificate_code": certificate.certificate_code,
            "average_score": float(
                certificate.average_score
            ),
            "lessons_completed": certificate.lessons_completed,
            "issued_at": getattr(
                certificate,
                "issued_at",
                None,
            ),
            "is_valid": getattr(
                certificate,
                "is_valid",
                True,
            ),
        })

    return {
        "certificates_earned": len(certificate_data),
        "certificate_status": (
            "Certified"
            if certificate_data
            else "Not Certified"
        ),
        "certificates": certificate_data,
    }