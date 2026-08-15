import csv
import io

from app.schemas.lesson_schema import LessonCreate
from app.services.lesson_service import create_lesson
from sqlalchemy.orm import Session

from db.models.users import User


class AdminService:

    @staticmethod
    def upload_lessons_csv(db: Session, file):

        content = file.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))

        uploaded = []

        for row in reader:
            lesson = LessonCreate(
                course_id=row["course_id"],
                letter=row["letter"],
                title=row["title"],
                description=row.get("description"),
                reference_image_url=row.get("reference_image_url"),
                order_index=int(row["order_index"]),
            )

            uploaded.append(create_lesson(db, lesson))

        return {
            "message": f"{len(uploaded)} lessons uploaded successfully",
            "count": len(uploaded),
        }

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

        return {"message": "User deleted successfully"}
