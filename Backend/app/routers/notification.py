from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(
    tags=["Notifications"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    return NotificationService.create_notification(db, notification)


@router.get(
    "/{user_id}",
    response_model=list[NotificationResponse],
)
def get_user_notifications(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    return NotificationService.get_user_notifications(db, user_id)


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_as_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return NotificationService.mark_as_read(db, notification_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
