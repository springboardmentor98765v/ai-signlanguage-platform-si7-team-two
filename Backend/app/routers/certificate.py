from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services.integration_service import IntegrationService

router = APIRouter()


@router.get("/eligibility/{user_id}")
def get_certificate_eligibility(user_id: str):
    try:
        return IntegrationService.get_certificate_eligibility(user_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/issue/{user_id}")
def issue_certificate(
    user_id: str,
    learner_name: str,
):
    try:
        pdf = IntegrationService.issue_certificate(
            user_id,
            learner_name,
        )

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f'attachment; filename="Certificate_{learner_name}.pdf"'
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )