from services.scoring import calculate_scores

# Test 1: correct sign, high confidence, held long enough
result1 = calculate_scores("A", "A", 0.95, duration_seconds=3.0)
print("Test 1 (correct, high confidence):", result1)
assert result1["is_correct"] is True

# Test 2: wrong sign predicted
result2 = calculate_scores("A", "B", 0.90, duration_seconds=3.0)
print("Test 2 (wrong sign):", result2)
assert result2["is_correct"] is False

# Test 3: correct sign but held too briefly
result3 = calculate_scores("A", "A", 0.95, duration_seconds=1.0)
print("Test 3 (correct but too quick):", result3)

print("\nAll tests passed!")