from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
import requests

from sqlalchemy.orm import Session

from app.core.security import require_learner
from app.database.database import get_db
from app.schemas.analytics_schema import AnalyticsSummaryResponse
from app.services.analytics_service import get_summary_for_learner
from app.services.integration_service import IntegrationService

router = APIRouter()


@router.get("/{user_id}/summary", response_model=AnalyticsSummaryResponse)
def get_persisted_summary(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_learner),
):
    """Return the authenticated learner's persisted analytics_summary row."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own analytics summary",
        )

    return get_summary_for_learner(db, user_id)


@router.get("/{user_id}")
def get_progress_report(user_id: str):
    try:
        return IntegrationService.get_progress_report(user_id)

    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text

        raise HTTPException(
            status_code=e.response.status_code,
            detail=detail,
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
