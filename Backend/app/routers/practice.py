from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx

router = APIRouter()

AI_SERVICE_URL = "http://127.0.0.1:8001/predict"


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = await file.read()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                AI_SERVICE_URL,
                files={
                    "file": (
                        file.filename,
                        image,
                        file.content_type,
                    )
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )

        return response.json()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"AI service unavailable: {str(e)}",
        )