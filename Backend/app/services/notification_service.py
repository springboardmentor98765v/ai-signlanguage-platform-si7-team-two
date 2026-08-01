from uuid import UUID

from app.schemas.notification import (
    NotificationCreate,
)


class NotificationService:

    @staticmethod
    def create_notification(notification: NotificationCreate):
        """
        Placeholder implementation.
        Will be updated once Notification model is available.
        """
        return {
            "message": "Notification created successfully",
            "notification": notification,
        }

    @staticmethod
    def get_user_notifications(user_id: UUID):
        """
        Placeholder implementation.
        """
        return {
            "user_id": user_id,
            "notifications": [],
        }

    @staticmethod
    def mark_as_read(notification_id: UUID):
        """
        Placeholder implementation.
        """
        return {
            "message": "Notification marked as read",
            "notification_id": notification_id,
        }
