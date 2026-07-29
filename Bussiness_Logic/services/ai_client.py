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
    Falls back to a safe mock response if the service is unreachable.
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
    except Exception as e:
        print(f"[WARN] AI service unreachable, using mock response: {e}")
        return {
            "predicted_sign": "A",
            "confidence": 0.85,
            "possible_issue": "No major issue detected.",
        }