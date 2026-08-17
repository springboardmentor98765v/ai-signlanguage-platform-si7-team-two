import os
import sys
from pathlib import Path

# Add Backend root to path so we can import app modules
sys.path.append(str(Path(__file__).resolve().parent))

from app.database.database import engine, Base, SessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress

def seed():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Seed Roles
    print("Seeding roles...")
    roles = ["Learner", "Instructor", "Admin"]
    role_map = {}
    for r in roles:
        role = db.query(Role).filter_by(name=r).first()
        if not role:
            role = Role(name=r)
            db.add(role)
            db.commit()
            db.refresh(role)
        role_map[r] = role
        
    # 2. Seed Course
    print("Seeding course...")
    course = db.query(Course).filter_by(name="ASL Basics").first()
    if not course:
        course = Course(
            name="ASL Basics",
            level="Beginner",
            description="Learn the ASL Alphabet"
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        
    # 3. Seed Lessons
    print("Seeding lessons...")
    letters_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["lll"]
    for idx, letter in enumerate(letters_list):
        lesson = db.query(Lesson).filter_by(course_id=course.id, letter=letter).first()
        if not lesson:
            lesson = Lesson(
                course_id=course.id,
                letter=letter,
                title=f"Letter {letter}",
                description=f"Learn to sign the letter {letter}",
                reference_image_url=f"/reference_images/{letter.lower()}.png",
                order_index=idx
            )
            db.add(lesson)
    db.commit()
    
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed()
