import asyncio
from unittest.mock import AsyncMock, patch
from services.ai_client import get_ai_prediction


def test_get_ai_prediction_returns_mocked_result():
    """AI prediction should return the JSON payload from the AI service."""
    mock_response = {
        "predicted_sign": "A",
        "confidence": 0.95,
        "hand_shape_score": 88.0,
        "finger_position_score": 91.0,
        "timing_score": 85.0,
        "motion_score": 87.0,
        "position_score": 90.0,
        "overall_score": 88.2,
        "is_correct": True,
        "feedback": [],
    }

    async def _run():
        with patch(
            "services.ai_client.get_ai_prediction",
            new=AsyncMock(return_value=mock_response),
        ) as mock_fn:
            result = await mock_fn(b"test")
            assert result["predicted_sign"] == "A"
            assert result["overall_score"] == 88.2
            assert result["is_correct"] is True

    asyncio.run(_run())
