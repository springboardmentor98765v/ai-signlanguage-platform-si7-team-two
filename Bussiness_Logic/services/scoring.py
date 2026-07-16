"""
Scoring engine — Milestone 2, Day 2 upgrade.

Milestone 1 note (kept for context):
Intern 3's AI service currently only returns predicted_sign + confidence.
Real hand-shape/finger-position/motion sub-scores and a `possible_issue`
hint are an Intern 3 Day 7 deliverable (per SRS). Until then, motion_score
and position_score remain placeholder constants — this is documented
explicitly below instead of being silently hardcoded, and the weights are
centralized so upgrading later (Day 7+) only means changing this one
SCORING_WEIGHTS dict and the two placeholder lines, nothing else.
"""

# Centralized weights — sum must equal 1.0. Change here only; nothing else
# in this file should hardcode a weight number.
SCORING_WEIGHTS = {
    "hand_shape": 0.30,
    "finger_position": 0.25,
    "motion": 0.15,
    "timing": 0.15,
    "position": 0.15,
}

# Sanity check at import time — fails loudly if weights are ever mistyped
assert abs(sum(SCORING_WEIGHTS.values()) - 1.0) < 1e-6, "SCORING_WEIGHTS must sum to 1.0"

CORRECT_THRESHOLD = 70.0

# Placeholder values for sub-scores we can't compute yet (pre-Day-7).
# TODO(Day 7): replace with real values derived from Intern 3's
# `possible_issue` field once available.
PLACEHOLDER_MOTION_SCORE = 100.0
PLACEHOLDER_POSITION_SCORE = 90.0


def normalize_confidence(confidence: float) -> float:
    """Accept confidence from either AI convention: 0-1 or 0-100."""
    return max(0.0, min(100.0, confidence * 100 if confidence <= 1 else confidence))


def calculate_scores(
    expected_sign: str,
    predicted_sign: str,
    confidence: float,
    duration_seconds: float,
    expected_duration: float = 3.0,
) -> dict:
    """
    Weighted multi-parameter scoring (Milestone 2, Day 2).

    Same 5-part structure as Milestone 1, but weights are now centralized
    in SCORING_WEIGHTS instead of scattered as magic numbers in the
    formula, so future tuning (or Day 7's real sub-scores) is a one-line
    change.
    """
    confidence_percent = normalize_confidence(confidence)
    is_match = predicted_sign.strip().upper() == expected_sign.strip().upper()

    hand_shape_score = confidence_percent if is_match else confidence_percent * 0.30
    finger_position_score = confidence_percent if is_match else confidence_percent * 0.30
    motion_score = PLACEHOLDER_MOTION_SCORE
    timing_score = min(100.0, (duration_seconds / expected_duration) * 100)
    position_score = PLACEHOLDER_POSITION_SCORE

    overall_score = (
        hand_shape_score * SCORING_WEIGHTS["hand_shape"]
        + finger_position_score * SCORING_WEIGHTS["finger_position"]
        + motion_score * SCORING_WEIGHTS["motion"]
        + timing_score * SCORING_WEIGHTS["timing"]
        + position_score * SCORING_WEIGHTS["position"]
    )

    is_correct = overall_score >= CORRECT_THRESHOLD

    return {
        "hand_shape_score": round(hand_shape_score, 2),
        "finger_position_score": round(finger_position_score, 2),
        "motion_score": round(motion_score, 2),
        "timing_score": round(timing_score, 2),
        "position_score": round(position_score, 2),
        "overall_score": round(overall_score, 2),
        "is_correct": is_correct,
    }