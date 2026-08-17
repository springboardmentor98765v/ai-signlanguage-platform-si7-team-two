from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from models.accessibility_trainer_learner_mapping_model import AccessibilityTrainerLearnerMapping
from models.certification_exam_model import CertificationExam
from models.practice_model import User, PracticeSession
from models.analytics_model import AnalyticsSummary as LearnerAnalytics

router = APIRouter(
    prefix="/trainer",
    tags=["Accessibility Trainer"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{trainer_id}/learners")
def get_assigned_learners(trainer_id: str, db: Session = Depends(get_db)):
    # Verify the trainer exists (maybe check role, but we assume the frontend sends a valid trainer_id for now)
    trainer = db.query(User).filter(User.id == trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
        
    mappings = db.query(AccessibilityTrainerLearnerMapping).filter(
        AccessibilityTrainerLearnerMapping.trainer_id == trainer_id
    ).all()
    
    learner_ids = [m.learner_id for m in mappings]
    learners = db.query(User).filter(User.id.in_(learner_ids)).all()
    
    results = []
    for learner in learners:
        # Engagement: total practice sessions and time
        sessions = db.query(PracticeSession).filter(PracticeSession.user_id == learner.id).all()
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.status == "completed"])
        
        # Skill Development / Assessment Analytics
        analytics = db.query(LearnerAnalytics).filter(LearnerAnalytics.user_id == learner.id).first()
        average_accuracy = float(analytics.average_accuracy) if analytics else 0.0
        
        # Certification status
        latest_exam = db.query(CertificationExam).filter(
            CertificationExam.learner_id == learner.id
        ).order_by(CertificationExam.taken_at.desc()).first()
        
        certification_status = "None"
        if latest_exam:
            certification_status = f"{latest_exam.level} - {'Passed' if latest_exam.is_passed else 'Failed'}"
            
        results.append({
            "id": learner.id,
            "full_name": learner.full_name,
            "email": learner.email,
            "engagement": {
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions
            },
            "analytics": {
                "average_accuracy": average_accuracy
            },
            "certification_status": certification_status
        })
        
    return results

@router.post("/{trainer_id}/assign/{learner_id}")
def assign_learner(trainer_id: str, learner_id: str, db: Session = Depends(get_db)):
    existing = db.query(AccessibilityTrainerLearnerMapping).filter(
        AccessibilityTrainerLearnerMapping.trainer_id == trainer_id,
        AccessibilityTrainerLearnerMapping.learner_id == learner_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Learner already assigned to this trainer")
        
    mapping = AccessibilityTrainerLearnerMapping(
        trainer_id=trainer_id,
        learner_id=learner_id
    )
    db.add(mapping)
    db.commit()
    return {"message": "Learner assigned successfully"}
