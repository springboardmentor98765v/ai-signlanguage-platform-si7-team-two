from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx

router = APIRouter()

AI_SERVICE_URL = "http://127.0.0.1:8001/predict"


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = await file.read()

        async with httpx.AsyncClient() as client:
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

        return response.json()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
