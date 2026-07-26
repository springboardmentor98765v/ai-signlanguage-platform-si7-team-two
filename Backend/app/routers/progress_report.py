from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import requests
from app.services.integration_service import IntegrationService

router = APIRouter()


@router.get("/{user_id}")
def get_progress_report(user_id: str):
    try:
        return IntegrationService.get_progress_report(user_id)

    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.json().get("detail", "Unknown error"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/{user_id}/download")
def download_progress_report(
    user_id: str,
    learner_name: str,
):

    try:
        pdf = IntegrationService.download_progress_report(
            user_id,
            learner_name,
        )

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f'attachment; filename="Progress_Report_{learner_name}.pdf"'
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )