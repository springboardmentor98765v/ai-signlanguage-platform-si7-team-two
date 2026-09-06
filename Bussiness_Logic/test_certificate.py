from services.certificate_engine import (
    check_certificate_eligibility,
    generate_certificate_code,
)
from types import SimpleNamespace


def make_session(letter):
    return SimpleNamespace(expected_sign=letter)


def make_assessment(score):
    return SimpleNamespace(overall_score=score)


required_letters = ["A", "B", "C"]


# Test 1: eligible learner
sessions_eligible = [
    make_session("A"),
    make_session("B"),
    make_session("C"),
]

assessments_eligible = [
    make_assessment(90),
    make_assessment(85),
    make_assessment(82),
]

result1 = check_certificate_eligibility(
    sessions_eligible,
    assessments_eligible,
    required_letters,
)

print("Test 1 (should be eligible):", result1)
assert result1["eligible"] is True


# Test 2: missing a letter
sessions_missing = [
    make_session("A"),
    make_session("B"),
]

assessments_missing = [
    make_assessment(95),
    make_assessment(90),
]

result2 = check_certificate_eligibility(
    sessions_missing,
    assessments_missing,
    required_letters,
)

print("Test 2 (should NOT be eligible - missing C):", result2)
assert result2["eligible"] is False
assert "C" in result2["missing_letters"]


# Test 3: low average score
sessions_low_score = [
    make_session("A"),
    make_session("B"),
    make_session("C"),
]

assessments_low_score = [
    make_assessment(60),
    make_assessment(65),
    make_assessment(70),
]

result3 = check_certificate_eligibility(
    sessions_low_score,
    assessments_low_score,
    required_letters,
)

print("Test 3 (should NOT be eligible - low average):", result3)
assert result3["eligible"] is False


# Test certificate code generation
code = generate_certificate_code(
    "12345678-aaaa-bbbb-cccc-111111111111"
)

print("\nSample certificate code:", code)

print("\nAll tests passed!")