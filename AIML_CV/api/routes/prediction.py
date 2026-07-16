from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

import cv2
import numpy as np

from services.recognizer import SignLanguageRecognizer
from api.schemas.prediction import PredictionResponse
from api.exceptions import AIServiceException
from config.logger import logger
router = APIRouter(
    tags=["Prediction"]
)

recognizer = SignLanguageRecognizer()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
async def predict(file: UploadFile = File(...)):
    logger.info("Prediction request received.")

    image_bytes = await file.read()

    np_image = np.frombuffer(image_bytes, np.uint8)

    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    if frame is None:
        logger.error("Invalid image uploaded.")
        raise AIServiceException(
            "Invalid image uploaded.",
            status_code=400
        )

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = recognizer.predict(rgb)
    if result["prediction"] == "No Hand":

        logger.warning("No hand detected.")

        raise AIServiceException(
            "No hand detected in the image.",
            status_code=400
        )
    response = PredictionResponse(
    prediction=result["prediction"],
    confidence=round(float(result["confidence"]) * 100, 2),
    possible_issue=result["possible_issue"]
)
    logger.info(
        f"Prediction: {result['prediction']} | Confidence: {result['confidence']:.4f}"
    )
    return response