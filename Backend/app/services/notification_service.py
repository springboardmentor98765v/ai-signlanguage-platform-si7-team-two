from uuid import UUID

from sqlalchemy.orm import Session

from db.models.notifications import Notification
from app.schemas.notification import NotificationCreate


class NotificationService:

    @staticmethod
    def create_notification(db: Session, notification: NotificationCreate):
        new_notification = Notification(
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
        )

        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)

        return new_notification

    @staticmethod
    def get_user_notifications(db: Session, user_id: UUID):
        notifications = (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

        return notifications

    @staticmethod
    def mark_as_read(db: Session, notification_id: UUID):
        notification = (
            db.query(Notification).filter(Notification.id == notification_id).first()
        )

        if notification is None:
            raise ValueError("Notification not found")

        notification.is_read = True

        db.commit()
        db.refresh(notification)

        return notification
