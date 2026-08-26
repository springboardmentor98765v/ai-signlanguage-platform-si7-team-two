import os
import httpx
from dotenv import load_dotenv

load_dotenv()

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8001")

def _normalize_sign(value: str) -> str:
    """Ensure predicted sign fits the DB's varchar(2) column."""
    if not value:
        return "?"
    value = value.strip().upper()
    return value[:2] if len(value) > 2 else value

async def get_ai_prediction(image_bytes: bytes, filename: str = "frame.jpg") -> dict:
    """
    Calls Intern 3's real AI service (POST /predict, multipart/form-data).
    Returns predicted_sign, confidence (0-1 scale), and possible_issue.

    Raises httpx.HTTPError (or HTTPException via the FastAPI handler) when
    the AI service is unreachable, times out, or returns an error response.
    The frontend treats these as service-down, retries once, and falls back
    to its own demo-mode banner — the learner is never silently shown fake
    "real" predictions.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            files = {"file": (filename, image_bytes, "image/jpeg")}
            response = await client.post(f"{AI_SERVICE_URL}/predict", files=files)
            response.raise_for_status()
            data = response.json()

            return {
                "predicted_sign": _normalize_sign(data["prediction"]),
                "confidence": data["confidence"] / 100.0,
                "possible_issue": data.get("possible_issue", "No major issue detected."),
            }
    except httpx.HTTPError as e:
        # Surface the failure honestly — don't pretend the AI succeeded.
        print(f"[WARN] AI service unreachable: {e}")
        raise