import pytest

from services.certification_exam_service import (
    CERTIFICATION_LEVELS,
    calculate_exam_score,
    create_certification_exam,
    get_exam_structure,
    evaluate_certification_exam,
    generate_certificate_after_exam,
)


# ---------------------------------------------------------
# TEST 1 - BEGINNER EXAM STRUCTURE
# ---------------------------------------------------------

def test_beginner_exam_structure():

    exam = get_exam_structure("Beginner")

    assert exam["level"] == "Beginner"
    assert exam["total_signs"] == 5
    assert len(exam["signs"]) == 5


# ---------------------------------------------------------
# TEST 2 - SCORE CALCULATION
# ---------------------------------------------------------

def test_exam_score_calculation():

    scores = [80, 90, 70, 80, 80]

    score = calculate_exam_score(scores)

    assert score == 80.0


# ---------------------------------------------------------
# TEST 3 - PASSING EXAM
# ---------------------------------------------------------

def test_beginner_exam_passes():

    scores = [80, 85, 90, 75, 80]

    result = evaluate_certification_exam(
        "Beginner",
        scores,
    )

    assert result.average_score == 82.0
    assert result.threshold == 70.0
    assert result.passed is True


# ---------------------------------------------------------
# TEST 4 - FAILING EXAM
# ---------------------------------------------------------

def test_beginner_exam_fails():

    scores = [50, 60, 55, 65, 60]

    result = evaluate_certification_exam(
        "Beginner",
        scores,
    )

    assert result.average_score == 58.0
    assert result.passed is False


# ---------------------------------------------------------
# TEST 5 - ALL FOUR LEVELS
# ---------------------------------------------------------

@pytest.mark.parametrize(
    "level",
    [
        "Beginner",
        "Intermediate",
        "Advanced",
        "Professional",
    ],
)
def test_all_certification_levels(level):

    exam = get_exam_structure(level)

    assert exam["level"] == level
    assert exam["total_signs"] > 0
    assert exam["pass_threshold"] > 0


# ---------------------------------------------------------
# TEST 6 - INVALID LEVEL
# ---------------------------------------------------------

def test_invalid_level():

    with pytest.raises(ValueError):

        get_exam_structure("Expert")


# ---------------------------------------------------------
# TEST 7 - INVALID SCORE
# ---------------------------------------------------------

def test_invalid_score():

    with pytest.raises(ValueError):

        calculate_exam_score([80, 120, 70])

def test_passed_exam_generates_certificate(tmp_path, monkeypatch):

    generated = {}

    def fake_certificate_generator(
        learner_name,
        average_score,
        certificate_code,
    ):
        generated["learner_name"] = learner_name
        generated["average_score"] = average_score
        generated["certificate_code"] = certificate_code

        return "generated_certificates/TEST_CERT.pdf"

    monkeypatch.setattr(
        "services.certification_exam_service.generate_certificate_pdf",
        fake_certificate_generator,
    )

    result = generate_certificate_after_exam(
        learner_name="Testing",
        level="Beginner",
        scores=[80, 85, 90, 75, 80],
        certificate_code="TEST-CERT-001",
    )

    assert result["passed"] is True
    assert result["certificate_path"] == (
        "generated_certificates/TEST_CERT.pdf"
    )

    assert generated["learner_name"] == "Testing"
    assert generated["certificate_code"] == "TEST-CERT-001"