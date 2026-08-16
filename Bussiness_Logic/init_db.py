from database import Base, engine
from models.practice_model import *
from models.assessment_model import *
from models.streak_model import *
from models.badge_model import *
from models.feedback_model import *
from models.analytics_model import *
from models.certification_exam_model import *
from models.accessibility_trainer_learner_mapping_model import *

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
