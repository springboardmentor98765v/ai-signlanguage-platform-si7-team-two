from uuid import UUID

from sqlalchemy.orm import Session

from db.models.notifications import Notification
from app.schemas.notification_schema import NotificationCreate


def create_notification(db: Session, notification: NotificationCreate):
    db_notification = Notification(
        user_id=notification.user_id,
        message=notification.message,
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


def get_user_notifications(db: Session, user_id: UUID):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_notification_as_read(db: Session, notification_id: UUID):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification is None:
        return None

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification