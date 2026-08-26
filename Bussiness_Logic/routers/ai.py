from fastapi import APIRouter, File, HTTPException, UploadFile

import httpx

from services.ai_client import get_ai_prediction

router = APIRouter(prefix="/ai", tags=["AI Integration"])


@router.post("/predict")
async def predict_sign(frame: UploadFile = File(...)):
    """Expose Intern 3's prediction service using the frontend contract."""
    if not frame.content_type or not frame.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image frame.")

    image_bytes = await frame.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="The image frame is empty.")

    try:
        result = await get_ai_prediction(image_bytes, filename=frame.filename or "frame.jpg")
    except httpx.HTTPError:
        # Translate any AI-service reachability failure into a clean 503 so
        # the frontend's retry + demo-mode flow can detect it (the message
        # contains "service unavailable" which matches api.js isServiceDown).
        raise HTTPException(status_code=503, detail="AI service unavailable")

    return {
        "predicted_sign": result["predicted_sign"],
        "confidence": round(result["confidence"] * 100, 2),
    }
