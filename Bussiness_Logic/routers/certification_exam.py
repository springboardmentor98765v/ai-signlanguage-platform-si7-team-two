import uuid
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models.certification_exam_model import CertificationExam
from models.practice_model import Certificate, User
from services.certificate_engine import generate_certificate_code
from services.certificate_generator import generate_certificate_pdf
from services.notification_client import send_notification

router = APIRouter(
    prefix="/certification_exams",
    tags=["Certification Exams"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ExamSubmission(BaseModel):
    learner_id: str
    level: str
    scores: List[float]  # scores for each sign in the exam


@router.post("/submit")
def submit_exam(submission: ExamSubmission, db: Session = Depends(get_db)):
    if not submission.scores:
        raise HTTPException(status_code=400, detail="Scores cannot be empty")
        
    overall_score = sum(submission.scores) / len(submission.scores)
    
    # Pass thresholds based on level
    thresholds = {
        "Beginner": 60.0,
        "Intermediate": 70.0,
        "Advanced": 80.0,
        "Professional": 90.0,
    }
    
    if submission.level not in thresholds:
        raise HTTPException(status_code=400, detail="Invalid level")
        
    is_passed = overall_score >= thresholds[submission.level]
    
    exam = CertificationExam(
        learner_id=submission.learner_id,
        level=submission.level,
        score=overall_score,
        is_passed=is_passed
    )
    
    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    if is_passed:
        # Check if they already have a certificate for this level or overall?
        # The requirements say "feeding into the same Certificate PDF generator you built in Milestone 2"
        learner = db.query(User).filter(User.id == submission.learner_id).first()
        learner_name = learner.full_name if learner else "Learner"
        
        certificate_code = generate_certificate_code(submission.learner_id)
        
        certificate = Certificate(
            learner_id=submission.learner_id,
            average_score=overall_score,
            lessons_completed=len(submission.scores), # roughly proxying exam length
            certificate_code=certificate_code,
        )
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
        
        file_path = generate_certificate_pdf(
            learner_name,
            overall_score,
            certificate_code,
        )
        
        certificate.file_path = file_path
        exam.certificate_id = certificate.id
        db.commit()
        
        send_notification(
            user_id=submission.learner_id,
            title="Certification Exam Passed",
            message=f"Congratulations! You passed the {submission.level} exam with a score of {overall_score:.2f}.",
        )
        
        return {
            "message": "Exam passed and certificate generated",
            "exam_id": exam.id,
            "certificate_id": certificate.id,
            "score": overall_score,
            "is_passed": True
        }
    
    return {
        "message": "Exam failed. Keep practicing!",
        "exam_id": exam.id,
        "score": overall_score,
        "is_passed": False
    }

@router.get("/{exam_id}/certificate")
def get_exam_certificate(exam_id: str, db: Session = Depends(get_db)):
    exam = db.query(CertificationExam).filter(CertificationExam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
        
    if not exam.is_passed or not exam.certificate_id:
        raise HTTPException(status_code=400, detail="No certificate for this exam")
        
    certificate = db.query(Certificate).filter(Certificate.id == exam.certificate_id).first()
    if not certificate or not certificate.file_path:
        raise HTTPException(status_code=404, detail="Certificate file not found")
        
    learner = db.query(User).filter(User.id == exam.learner_id).first()
    learner_name = learner.full_name if learner else "Learner"
    
    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"Certificate_{learner_name}.pdf",
    )
