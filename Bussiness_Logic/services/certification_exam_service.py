"""
Certification Exam Service

Handles:
- Four certification levels
- Multi-sign exam structure
- Pass/fail calculation
- Reuses existing weighted scoring
- Triggers existing certificate generator after passing
"""
from typing import List, Dict
from dataclasses import dataclass
from services.certificate_generator import generate_certificate_pdf


# ---------------------------------------------------------
# 1. CERTIFICATION LEVEL CONFIGURATION
# ---------------------------------------------------------

CERTIFICATION_LEVELS = {
    "Beginner": {
        "signs": ["A", "B", "C", "D", "E"],
        "pass_threshold": 70.0,
    },
    "Intermediate": {
        "signs": ["F", "G", "H", "I", "J", "K", "L", "M"],
        "pass_threshold": 75.0,
    },
    "Advanced": {
        "signs": ["N", "O", "P", "Q", "R", "S", "T", "U"],
        "pass_threshold": 80.0,
    },
    "Professional": {
        "signs": ["V", "W", "X", "Y", "Z"],
        "pass_threshold": 85.0,
    },
}


# ---------------------------------------------------------
# 2. EXAM RESULT DATA MODEL
# ---------------------------------------------------------

@dataclass
class CertificationExamResult:
    level: str
    total_signs: int
    average_score: float
    threshold: float
    passed: bool


# ---------------------------------------------------------
# 3. GET EXAM STRUCTURE / CREATE EXAM
# ---------------------------------------------------------

def get_exam_structure(level: str) -> Dict:
    """
    Returns the signs and pass threshold for a certification level.
    """
    if level not in CERTIFICATION_LEVELS:
        raise ValueError(
            "Invalid certification level. "
            "Choose Beginner, Intermediate, Advanced or Professional."
        )

    config = CERTIFICATION_LEVELS[level]

    return {
        "level": level,
        "signs": config["signs"],
        "total_signs": len(config["signs"]),
        "pass_threshold": config["pass_threshold"],
    }


def create_certification_exam(level: str) -> Dict:
    """
    Creates a structured certification exam for the given level.
    """
    if level not in CERTIFICATION_LEVELS:
        raise ValueError("Invalid certification level.")

    config = CERTIFICATION_LEVELS[level]

    return {
        "level": level,
        "signs": config["signs"],
        "total_signs": len(config["signs"]),
        "pass_threshold": config["pass_threshold"],
    }


# ---------------------------------------------------------
# 4. CALCULATE EXAM SCORE
# ---------------------------------------------------------

def calculate_exam_score(scores: List[float]) -> float:
    """
    Calculates the overall certification exam score.
    Each sign score is expected to be between 0 and 100.
    """
    if not scores:
        raise ValueError("At least one sign score is required.")

    if any(score < 0 or score > 100 for score in scores):
        raise ValueError("Every score must be between 0 and 100.")

    return round(sum(scores) / len(scores), 2)


# ---------------------------------------------------------
# 5. EVALUATE CERTIFICATION EXAM
# ---------------------------------------------------------

def evaluate_certification_exam(
    level: str,
    scores: List[float],
) -> CertificationExamResult:
    """
    Evaluates a complete multi-sign certification exam against pass thresholds.
    """
    if level not in CERTIFICATION_LEVELS:
        raise ValueError("Invalid certification level.")

    config = CERTIFICATION_LEVELS[level]
    expected_sign_count = len(config["signs"])

    if len(scores) != expected_sign_count:
        raise ValueError(
            f"{level} exam requires {expected_sign_count} sign scores."
        )

    average_score = calculate_exam_score(scores)
    threshold = config["pass_threshold"]
    passed = average_score >= threshold

    return CertificationExamResult(
        level=level,
        total_signs=expected_sign_count,
        average_score=average_score,
        threshold=threshold,
        passed=passed,
    )


# ---------------------------------------------------------
# 6. TRIGGER CERTIFICATE GENERATION
# ---------------------------------------------------------

def generate_certificate_after_exam(
    learner_name: str,
    level: str,
    scores: List[float],
    certificate_code: str,
) -> Dict:
    """
    Evaluates the certification exam.
    If passed, generates the existing certificate PDF.
    """
    result = evaluate_certification_exam(
        level=level,
        scores=scores,
    )

    if not result.passed:
        return {
            "passed": False,
            "certificate_path": None,
            "exam_result": result,
        }

    certificate_path = generate_certificate_pdf(
        learner_name=learner_name,
        average_score=result.average_score,
        certificate_code=certificate_code,
    )

    return {
        "passed": True,
        "certificate_path": certificate_path,
        "exam_result": result,
    }