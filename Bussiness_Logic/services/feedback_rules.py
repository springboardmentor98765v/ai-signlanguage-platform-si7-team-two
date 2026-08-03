"""
Rule-based feedback engine — Milestone 2, Day 3.

Uses Intern 3's real, landmark-based `possible_issue` message directly
for hand-shape/finger-position/position feedback, instead of a separate
guessed tips dictionary.

IMPORTANT: Intern 5's `feedback` table only allows these categories:
('hand_shape', 'timing', 'position', 'motion') — no 'finger_position' or
'gesture_accuracy'. So any AI-issue-driven feedback is tagged as
'hand_shape' here, since that's the closest allowed category for
gesture/shape corrections.
"""

import random

THRESHOLD = 70.0
EXCELLENT_THRESHOLD = 90.0

NON_ISSUE_MESSAGES = {
    "No major issue detected.",
}

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    NON_ISSUE_MESSAGES.add(f"Good '{letter}' hand shape.")

ENCOURAGEMENT_MESSAGES = [
    "Excellent! Your sign was very accurate.",
    "Great job, that was a clean and clear sign!",
    "Nailed it! Keep practicing to build consistency.",
    "Well done — your hand shape and timing were spot on.",
]

GOOD_JOB_MESSAGES = [
    "Good job! Keep practicing to improve further.",
    "Nice attempt — a little more practice and this will be perfect.",
    "You're close! Keep working on it.",
]


def generate_feedback(scores: dict, possible_issue: str = None) -> list:
    """
    scores: hand_shape_score, finger_position_score, timing_score,
    motion_score, position_score, overall_score.
    possible_issue: real, landmark-based hint from Intern 3's AI service.
    """
    feedback = []

    gesture_needs_correction = (
        scores["hand_shape_score"] < THRESHOLD
        or scores["finger_position_score"] < THRESHOLD
        or scores["position_score"] < THRESHOLD
    )
    if gesture_needs_correction and possible_issue and possible_issue not in NON_ISSUE_MESSAGES:
        feedback.append({
            "category": "hand_shape",  # only allowed category for gesture/shape issues
            "severity": "major" if scores["hand_shape_score"] < 50 else "moderate",
            "message": possible_issue,
        })

    if scores["timing_score"] < THRESHOLD:
        feedback.append({
            "category": "timing",
            "severity": "minor",
            "message": "Hold the gesture a bit longer before releasing.",
        })

    if scores["motion_score"] < THRESHOLD:
        feedback.append({
            "category": "motion",
            "severity": "moderate",
            "message": "Movement was too fast or unclear — slow down.",
        })

    if not feedback:
        if scores["overall_score"] >= EXCELLENT_THRESHOLD:
            message = random.choice(ENCOURAGEMENT_MESSAGES)
        else:
            message = random.choice(GOOD_JOB_MESSAGES)
        feedback.append({
            "category": "hand_shape",
            "severity": None,
            "message": message,
        })

    return feedback