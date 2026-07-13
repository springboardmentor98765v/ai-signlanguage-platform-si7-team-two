"""
Rule-based feedback engine for Milestone 1.
Maps low sub-scores from an assessment into specific, human-readable
correction messages. Each rule returns (category, severity, message).
"""

THRESHOLD = 70.0
EXCELLENT_THRESHOLD = 90.0

def generate_feedback(scores: dict) -> list:
    """
    scores expects the 5 sub-score keys from the assessment:
    hand_shape_score, finger_position_score, timing_score,
    motion_score, position_score, overall_score
    """
    feedback = []

    if scores["hand_shape_score"] < THRESHOLD:
        feedback.append({
            "category": "hand_shape",
            "severity": "major" if scores["hand_shape_score"] < 50 else "moderate",
            "message": "Your overall hand shape doesn't match — check the reference image again."
        })

    if scores["finger_position_score"] < THRESHOLD:
        feedback.append({
            "category": "finger_position",
            "severity": "major" if scores["finger_position_score"] < 50 else "moderate",
            "message": "Some fingers aren't positioned correctly — adjust and retry."
        })

    if scores["timing_score"] < THRESHOLD:
        feedback.append({
            "category": "timing",
            "severity": "minor",
            "message": "Hold the gesture a bit longer before releasing."
        })

    if scores["motion_score"] < THRESHOLD:
        feedback.append({
            "category": "motion",
            "severity": "moderate",
            "message": "Movement was too fast or unclear — slow down."
        })

    if scores["position_score"] < THRESHOLD:
        feedback.append({
            "category": "position",
            "severity": "minor",
            "message": "Move your hand more into the center of the frame."
        })

    # No issues found — give positive reinforcement
    if not feedback:
        if scores["overall_score"] >= EXCELLENT_THRESHOLD:
            feedback.append({
                "category": "hand_shape",
                "severity": None,
                "message": "Excellent! Your sign was very accurate."
            })
        else:
            feedback.append({
                "category": "hand_shape",
                "severity": None,
                "message": "Good job! Keep practicing to improve further."
            })

    return feedback