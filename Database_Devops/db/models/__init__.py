"""
db/models/__init__.py

Full schema, as of Day 4 (SRS §6, Intern 5, Days 3-4). Import from this
package (not the individual files) so relationship() string references
resolve correctly, e.g.:
    from db.models import Base, Role, User, Course, Lesson, PracticeSession, Assessment, Feedback, LearnerAnalytics
"""
from db.models.base import Base
from db.models.roles import Role
from db.models.users import User
from db.models.courses import Course
from db.models.lessons import Lesson
from db.models.practice_sessions import PracticeSession
from db.models.assessments import Assessment
from db.models.feedback import Feedback
from db.models.learner_analytics import LearnerAnalytics

__all__ = [
    "Base",
    "Role",
    "User",
    "Course",
    "Lesson",
    "PracticeSession",
    "Assessment",
    "Feedback",
    "LearnerAnalytics",
]
