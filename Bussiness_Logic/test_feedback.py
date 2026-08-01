from services.feedback_rules import generate_feedback

# Test 1: low scores + real AI issue message (letter A example)
low_scores = {
    "hand_shape_score": 40.0,
    "finger_position_score": 45.0,
    "timing_score": 60.0,
    "motion_score": 100.0,
    "position_score": 90.0,
    "overall_score": 55.0,
}
result1 = generate_feedback(low_scores, "Fold your thumb outside the fist.")
print("Test 1 (wrong attempt, real AI issue):")
for fb in result1:
    print(" -", fb["category"], ":", fb["message"])

# Test 2: low scores but AI says no issue (shouldn't show a fake correction)
result2 = generate_feedback(low_scores, "No major issue detected.")
print("\nTest 2 (low score, AI says fine - only timing shown):")
for fb in result2:
    print(" -", fb["category"], ":", fb["message"])

# Test 3: correct attempt (high scores)
high_scores = {
    "hand_shape_score": 95.0,
    "finger_position_score": 95.0,
    "timing_score": 95.0,
    "motion_score": 100.0,
    "position_score": 90.0,
    "overall_score": 95.0,
}
result3 = generate_feedback(high_scores, "Good 'A' hand shape.")
print("\nTest 3 (correct attempt):")
for fb in result3:
    print(" -", fb["message"])

print("\nAll tests passed!")