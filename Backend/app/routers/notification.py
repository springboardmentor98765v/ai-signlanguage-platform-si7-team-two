from uuid import UUID

from fastapi import APIRouter

from app.schemas.notification import NotificationCreate
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("/")
def create_notification(notification: NotificationCreate):
    return NotificationService.create_notification(notification)


@router.get("/{user_id}")
def get_user_notifications(user_id: UUID):
    return NotificationService.get_user_notifications(user_id)


@router.put("/{notification_id}/read")
def mark_as_read(notification_id: UUID):
    return NotificationService.mark_as_read(notification_id)
