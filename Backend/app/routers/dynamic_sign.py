from uuid import UUID

import httpx

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends,
    Form,
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.dynamic_sign_attempt import DynamicSignAttempt


router = APIRouter()


# Dynamic prediction endpoint in AI service
AI_DYNAMIC_SERVICE_URL = "http://127.0.0.1:8001/predict-dynamic"


@router.post("/dynamic/predict")
async def predict_dynamic_sign(
    file: UploadFile = File(...),

    user_id: UUID = Form(...),

    practice_session_id: UUID = Form(...),

    expected_word: str = Form(...),

    db: Session = Depends(get_db),
):

    try:

        image = await file.read()

        # Send image to AI Service
        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                AI_DYNAMIC_SERVICE_URL,

                files={
                    "file": (
                        file.filename,
                        image,
                        file.content_type,
                    )
                },
            )


        # Handle AI errors
        if response.status_code != 200:

            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )


        ai_result = response.json()


        # If dynamic model still collecting frames
        if not ai_result.get("ready", False):

            return ai_result


        predicted_word = ai_result.get("prediction")

        confidence = ai_result.get(
            "confidence",
            0,
        )


        if not predicted_word:

            raise HTTPException(
                status_code=500,
                detail="AI service did not return prediction",
            )


        # Compare prediction
        is_correct = (

            expected_word.strip().lower()

            ==

            predicted_word.strip().lower()

        )


        # Save attempt
        dynamic_attempt = DynamicSignAttempt(

            user_id=user_id,

            practice_session_id=practice_session_id,

            expected_word=expected_word,

            predicted_word=predicted_word,

            confidence=float(confidence),

            is_correct=is_correct,

        )


        db.add(dynamic_attempt)

        db.commit()

        db.refresh(dynamic_attempt)


        return {

            "ready": True,

            "prediction": predicted_word,

            "confidence": confidence,

            "is_correct": is_correct,

            "attempt_id": str(dynamic_attempt.id),

            "frames_collected": ai_result.get(
                "frames_collected"
            ),

            "frames_required": ai_result.get(
                "frames_required"
            ),

        }


    except httpx.RequestError as e:

        raise HTTPException(

            status_code=503,

            detail=f"AI service unavailable: {str(e)}",

        )


    except HTTPException:

        raise


    except Exception as e:

        db.rollback()

        raise HTTPException(

            status_code=500,

            detail=f"Prediction processing failed: {str(e)}",

        )