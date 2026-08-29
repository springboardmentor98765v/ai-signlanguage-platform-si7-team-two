from fastapi import APIRouter, UploadFile, File

import cv2
import mediapipe as mp
import numpy as np

from services.dynamic_recognizer import DynamicSignRecognizer
from api.exceptions import AIServiceException
from config.logger import logger


router = APIRouter(
    tags=["Dynamic Prediction"]
)


# ============================================================
# MEDIAPIPE HOLISTIC
# ============================================================

mp_holistic = mp.solutions.holistic

holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    smooth_segmentation=False,
    refine_face_landmarks=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ============================================================
# DYNAMIC RECOGNIZER
# ============================================================

recognizer = DynamicSignRecognizer()


# ============================================================
# DYNAMIC PREDICTION ENDPOINT
# ============================================================

@router.post(
    "/predict-dynamic"
)
async def predict_dynamic(
    file: UploadFile = File(...)
):

    logger.info(
        "Dynamic prediction frame received."
    )


    # --------------------------------------------------------
    # READ IMAGE
    # --------------------------------------------------------

    image_bytes = await file.read()

    np_image = np.frombuffer(
        image_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        np_image,
        cv2.IMREAD_COLOR
    )


    if frame is None:

        raise AIServiceException(
            "Invalid image uploaded.",
            status_code=400
        )


    # --------------------------------------------------------
    # BGR → RGB
    # --------------------------------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------------------------------
    # MEDIAPIPE HOLISTIC
    # --------------------------------------------------------

    results = holistic.process(
        rgb_frame
    )


    # --------------------------------------------------------
    # ADD FRAME TO SEQUENCE
    # --------------------------------------------------------

    try:

        frames_collected = recognizer.add_frame(
            results
        )

    except Exception as error:

        logger.error(
            f"Feature extraction error: {error}"
        )

        raise AIServiceException(
            str(error),
            status_code=500
        )


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    result = recognizer.predict()


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "ready": result["ready"],
        "frames_collected": result[
            "frames_collected"
        ],
        "frames_required": result[
            "frames_required"
        ],
        "prediction": result["prediction"],
        "confidence": result["confidence"]
    }