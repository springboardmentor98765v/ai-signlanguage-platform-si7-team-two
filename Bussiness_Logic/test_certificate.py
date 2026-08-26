from services.certificate_engine import check_certificate_eligibility, generate_certificate_code
from types import SimpleNamespace


def make_session(letter):
    return SimpleNamespace(expected_sign=letter)


def make_assessment(score):
    return SimpleNamespace(overall_score=score)


required_letters = ["A", "B", "C"]


def test_certificate_eligible_learner():
    """All letters attempted and average score >= 80 => eligible."""
    sessions = [make_session("A"), make_session("B"), make_session("C")]
    assessments = [make_assessment(90), make_assessment(85), make_assessment(82)]
    result = check_certificate_eligibility(sessions, assessments, required_letters)
    print("Test 1 (should be eligible):", result)
    assert result["eligible"] is True


def test_certificate_missing_letter():
    """Missing required letter => not eligible."""
    sessions = [make_session("A"), make_session("B")]
    assessments = [make_assessment(95), make_assessment(90)]
    result = check_certificate_eligibility(sessions, assessments, required_letters)
    print("Test 2 (should NOT be eligible - missing C):", result)
    assert result["eligible"] is False
    assert "C" in result["missing_letters"]


def test_certificate_low_average():
    """All letters attempted but average score < 80 => not eligible."""
    sessions = [make_session("A"), make_session("B"), make_session("C")]
    assessments = [make_assessment(60), make_assessment(65), make_assessment(70)]
    result = check_certificate_eligibility(sessions, assessments, required_letters)
    print("Test 3 (should NOT be eligible - low average):", result)
    assert result["eligible"] is False


def test_certificate_code_generation():
    """Certificate code should start with CERT-."""
    code = generate_certificate_code("12345678-aaaa-bbbb-cccc-111111111111")
    print("\nSample certificate code:", code)
    assert code.startswith("CERT-")