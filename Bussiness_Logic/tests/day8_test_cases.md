# Milestone 3 - Day 8 Test Cases

## Test Case 1 – Excellent Learner

**Scenario:**
Learner performs all signs correctly with high confidence and good timing.

**Expected Result:**
- Overall score greater than 90
- Positive feedback generated
- No recommendation generated
- Badge awarded (if eligible)
- Streak updated successfully

---

## Test Case 2 – Weak Performance on a Letter

**Scenario:**
Learner repeatedly performs the letter Z with low accuracy.

**Expected Result:**
- Overall score below threshold
- Corrective feedback generated
- Recommendation created for letter Z
- No badge awarded

---

## Test Case 3 – Inconsistent Performance

**Scenario:**
Learner performs some attempts correctly and others incorrectly.

**Expected Result:**
- Recency-weighted recommendation logic is applied
- Feedback reflects recent performance
- Recommendation generated if weighted score is below threshold

---

## Test Case 4 – Certificate Generation

**Scenario:**
Learner completes all required lessons with sufficient average score.

**Expected Result:**
- Certificate eligibility becomes true
- Certificate PDF generated
- Certificate notification created

---

## Test Case 5 – Badge and Streak Update

**Scenario:**
Learner practices on consecutive days and meets badge criteria.

**Expected Result:**
- Streak count increases
- Badge unlocked
- Badge notification created