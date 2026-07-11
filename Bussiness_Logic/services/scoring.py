def calculate_scores(expected_sign: str, predicted_sign: str, confidence: float, duration_seconds: float, expected_duration: float = 3.0):
    """
    Bootstrapped scoring logic for Milestone 1.
    Intern 3's AI service currently only provides predicted_sign + confidence
    (their FastAPI wrapper is a Day 6 task per SRS). Sub-scores below are
    derived from confidence + timing until real landmark-based sub-scores
    are available.
    """
    is_match = predicted_sign == expected_sign

    hand_shape_score = confidence * 100 if is_match else confidence * 30
    finger_position_score = confidence * 100 if is_match else confidence * 30
    motion_score = 100.0  # static letters assumed fine for M1
    timing_score = min(100.0, (duration_seconds / expected_duration) * 100)
    position_score = 90.0  # placeholder until real landmark data available

    overall_score = (
        hand_shape_score * 0.30 +
        finger_position_score * 0.25 +
        motion_score * 0.15 +
        timing_score * 0.15 +
        position_score * 0.15
    )

    is_correct = overall_score >= 70

    return {
        "hand_shape_score": round(hand_shape_score, 2),
        "finger_position_score": round(finger_position_score, 2),
        "motion_score": round(motion_score, 2),
        "timing_score": round(timing_score, 2),
        "position_score": round(position_score, 2),
        "overall_score": round(overall_score, 2),
        "is_correct": is_correct
    }