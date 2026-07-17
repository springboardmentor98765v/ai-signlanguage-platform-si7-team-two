"""
Rule-based feedback engine — Milestone 2, Day 3 upgrade.

Intern 3's AI service already analyzes real hand landmarks and returns a
`possible_issue` message specific to the letter being attempted (e.g.
"Fold your thumb outside the fist." for letter A). That single message
already covers hand-shape, finger-position, AND hand-position-in-frame
issues combined — so instead of maintaining our own guessed per-letter
tips (which would be less accurate), we use their message directly.

We only add our own feedback for things the AI can't see from a single
frame: timing (held too briefly) and motion (too fast/unclear), which
depend on session duration data we own.
"""

THRESHOLD = 70.0
EXCELLENT_THRESHOLD = 90.0

# Messages from the AI service that mean "nothing wrong" — don't show
# these as a correction, they're not useful feedback.
NON_ISSUE_MESSAGES = {
    "No major issue detected.",
    "Good 'A' hand shape.",
    "Good 'B' hand shape.",
    "Good 'C' hand shape.",
    "Good 'D' hand shape.",
    "Good 'E' hand shape.",
}

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
    scores: the 5 sub-score keys + overall_score.
    possible_issue: real, letter-specific hint from Intern 3's AI service
    (landmark-based), used directly instead of our own guessed tips.
    """
    feedback = []

    # Hand shape / finger position / hand-in-frame position issues —
    # all covered by the AI's possible_issue message in one go.
    gesture_needs_correction = (
        scores["hand_shape_score"] < THRESHOLD
        or scores["finger_position_score"] < THRESHOLD
        or scores["position_score"] < THRESHOLD
    )
    if gesture_needs_correction and possible_issue and possible_issue not in NON_ISSUE_MESSAGES:
        feedback.append({
            "category": "gesture_accuracy",
            "severity": "major" if scores["hand_shape_score"] < 50 else "moderate",
            "message": possible_issue,
        })

    # Timing and motion — not visible to the AI from a single frame,
    # so we keep our own generic checks for these.
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

    # No issues found — encouragement, rotated so it's not always the same line
    if not feedback:
        import random
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