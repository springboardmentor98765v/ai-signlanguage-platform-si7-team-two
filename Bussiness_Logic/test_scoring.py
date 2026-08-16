from services.scoring import calculate_scores


def test_correct_sign_high_confidence():
    """Correct sign with high confidence and sufficient duration."""

    result = calculate_scores(
        "A",
        "A",
        0.95,
        duration_seconds=3.0,
    )

    assert result["is_correct"] is True
    assert result["overall_score"] >= 70


def test_wrong_sign():
    """Wrong predicted sign should not be considered correct."""

    result = calculate_scores(
        "A",
        "B",
        0.90,
        duration_seconds=3.0,
    )

    assert result["is_correct"] is False


def test_correct_sign_short_duration():
    """Correct sign with a short duration is still calculated."""

    result = calculate_scores(
        "A",
        "A",
        0.95,
        duration_seconds=1.0,
    )

    assert "overall_score" in result
    assert "is_correct" in result


def test_score_values_are_valid():
    """All generated score components must be between 0 and 100."""

    result = calculate_scores(
        "A",
        "A",
        0.95,
        duration_seconds=3.0,
    )

    assert 0 <= result["hand_shape_score"] <= 100
    assert 0 <= result["finger_position_score"] <= 100
    assert 0 <= result["motion_score"] <= 100
    assert 0 <= result["timing_score"] <= 100
    assert 0 <= result["position_score"] <= 100
    assert 0 <= result["overall_score"] <= 100