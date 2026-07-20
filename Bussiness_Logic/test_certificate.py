from services.certificate_engine import check_certificate_eligibility, generate_certificate_code
from types import SimpleNamespace

def make_assessment(letter, score):
    return SimpleNamespace(expected_sign=letter, overall_score=score)

required_letters = ["A", "B", "C"]

# Test 1: eligible learner - all letters attempted, high average
assessments_eligible = [
    make_assessment("A", 90),
    make_assessment("B", 85),
    make_assessment("C", 82),
]
result1 = check_certificate_eligibility(assessments_eligible, required_letters)
print("Test 1 (should be eligible):", result1)
assert result1["eligible"] is True

# Test 2: missing a letter - not eligible even with high scores
assessments_missing = [
    make_assessment("A", 95),
    make_assessment("B", 90),
]
result2 = check_certificate_eligibility(assessments_missing, required_letters)
print("Test 2 (should NOT be eligible - missing C):", result2)
assert result2["eligible"] is False
assert "C" in result2["missing_letters"]

# Test 3: all letters attempted but average too low
assessments_low_score = [
    make_assessment("A", 60),
    make_assessment("B", 65),
    make_assessment("C", 70),
]
result3 = check_certificate_eligibility(assessments_low_score, required_letters)
print("Test 3 (should NOT be eligible - low average):", result3)
assert result3["eligible"] is False

# Test certificate code generation
code = generate_certificate_code("12345678-aaaa-bbbb-cccc-111111111111")
print("\nSample certificate code:", code)

print("\nAll tests passed!")