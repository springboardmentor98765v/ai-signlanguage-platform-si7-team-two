from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.notification_schema import NotificationCreate
from app.services.notification_service import (
    create_notification,
    get_user_notifications,
    mark_notification_as_read,
)

router = APIRouter()


@router.post("/")
def create(notification: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(db, notification)


@router.get("/{user_id}")
def get_notifications(user_id: UUID, db: Session = Depends(get_db)):
    return get_user_notifications(db, user_id)


@router.put("/{notification_id}/read")
def mark_read(notification_id: UUID, db: Session = Depends(get_db)):
    notification = mark_notification_as_read(db, notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return notification