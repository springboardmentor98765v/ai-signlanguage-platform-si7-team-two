from fastapi import APIRouter
from fastapi import HTTPException
import httpx

router = APIRouter()

BUSINESS_LOGIC_URL = "http://bussiness_logic:8002/assessment/score"

@router.post("/score")
async def score(payload: dict):

    try:

        async with httpx.AsyncClient() as client:

            response = await client.post(
                BUSINESS_LOGIC_URL,
                json=payload
            )

        return response.json()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )