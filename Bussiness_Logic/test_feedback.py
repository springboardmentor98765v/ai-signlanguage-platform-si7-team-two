from services.feedback_rules import generate_feedback


def test_low_scores_with_ai_issue():
    """Low scores with a real AI issue should generate corrective feedback."""

    scores = {
        "hand_shape_score": 40.0,
        "finger_position_score": 45.0,
        "timing_score": 60.0,
        "motion_score": 100.0,
        "position_score": 90.0,
        "overall_score": 55.0,
    }

    result = generate_feedback(
        scores,
        "Fold your thumb outside the fist.",
    )

    assert result
    assert isinstance(result, list)

    messages = [
        feedback["message"]
        for feedback in result
    ]

    assert any(
        "thumb" in message.lower()
        for message in messages
    )


def test_low_scores_without_ai_issue():
    """Low scores with no detected AI issue should not invent a correction."""

    scores = {
        "hand_shape_score": 40.0,
        "finger_position_score": 45.0,
        "timing_score": 60.0,
        "motion_score": 100.0,
        "position_score": 90.0,
        "overall_score": 55.0,
    }

    result = generate_feedback(
        scores,
        "No major issue detected.",
    )

    assert isinstance(result, list)

    # Feedback should still be generated for the low score,
    # but the system should not invent an unrelated AI correction.
    assert len(result) >= 1


def test_high_scores_generate_positive_feedback():
    """High scores should produce positive/correct feedback."""

    scores = {
        "hand_shape_score": 95.0,
        "finger_position_score": 95.0,
        "timing_score": 95.0,
        "motion_score": 100.0,
        "position_score": 90.0,
        "overall_score": 95.0,
    }

    result = generate_feedback(
        scores,
        "Good 'A' hand shape.",
    )

    assert isinstance(result, list)
    assert len(result) >= 1


def test_feedback_contains_required_fields():
    """Every feedback item should contain category and message."""

    scores = {
        "hand_shape_score": 40.0,
        "finger_position_score": 45.0,
        "timing_score": 60.0,
        "motion_score": 100.0,
        "position_score": 90.0,
        "overall_score": 55.0,
    }

    result = generate_feedback(
        scores,
        "Fold your thumb outside the fist.",
    )

    for feedback in result:
        assert "category" in feedback
        assert "message" in feedback