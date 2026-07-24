from sqlalchemy.orm import Session

from db.models.users import User


class AdminService:

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def delete_user(db: Session, user_id):
        user = db.get(User, user_id)

        if user is None:
            raise ValueError("User not found")

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }