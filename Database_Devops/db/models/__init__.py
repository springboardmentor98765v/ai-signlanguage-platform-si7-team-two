"""
db/models/__init__.py

Day 3 scope only: Roles, Users, Courses, Lessons (SRS §6, Intern 5, Day 3).
Practice Sessions, Assessments, Feedback, and Learner Analytics models are
Day 4 work and will be added to this package then — do not add them here
prematurely.

Import from this package (not the individual files) so relationship()
string references resolve correctly, e.g.:
    from db.models import Base, Role, User, Course, Lesson
"""
from db.models.base import Base
from db.models.roles import Role
from db.models.users import User
from db.models.courses import Course
from db.models.lessons import Lesson

__all__ = ["Base", "Role", "User", "Course", "Lesson"]
