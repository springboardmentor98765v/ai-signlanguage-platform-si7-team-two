from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession, Lesson, Certificate
from models.assessment_model import Assessment
from services.certificate_engine import check_certificate_eligibility, generate_certificate_code
from schemas.certificate_schema import CertificateEligibilityResponse, CertificateIssuedResponse
from uuid import UUID
from services.certificate_generator import generate_certificate_pdf

router = APIRouter(prefix="/certificates", tags=["Certificates"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{learner_id}/eligibility", response_model=CertificateEligibilityResponse)
def check_eligibility(learner_id: UUID, db: Session = Depends(get_db)):
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == learner_id).all()
    session_ids = [s.id for s in sessions]

    assessments = (
        db.query(Assessment).filter(Assessment.session_id.in_(session_ids)).all()
        if session_ids else []
    )

    required_letters = [
        l.letter for l in db.query(Lesson).all() if l.letter
    ]

    result = check_certificate_eligibility(assessments, required_letters)

    return {
        "learner_id": str(learner_id),
        **result,
    }


@router.post("/{learner_id}/issue", response_model=CertificateIssuedResponse)
def issue_certificate(learner_id: UUID, learner_name: str,db: Session = Depends(get_db)):
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == learner_id).all()
    session_ids = [s.id for s in sessions]

    assessments = (
        db.query(Assessment).filter(Assessment.session_id.in_(session_ids)).all()
        if session_ids else []
    )

    required_letters = [l.letter for l in db.query(Lesson).all() if l.letter]

    result = check_certificate_eligibility(assessments, required_letters)

    if not result["eligible"]:
        raise HTTPException(
            status_code=400,
            detail=f"Not eligible yet. Missing letters: {result['missing_letters']}, "
                   f"average score: {result['average_score']}"
        )

    completed_sessions = [s for s in sessions if s.status == "completed"]

    certificate_code = generate_certificate_code(learner_id)

    cert = Certificate(
        learner_id=learner_id,
        average_score=result["average_score"],
        lessons_completed=len(completed_sessions),
        certificate_code=certificate_code,
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    # Generate the actual PDF file and save its path
    # NOTE: learner_name is a placeholder here since this service doesn't
    # own the users table's full_name field — see note below.
   
    file_path = generate_certificate_pdf(learner_name, result["average_score"], certificate_code)

    cert.file_path = file_path
    db.commit()
    db.refresh(cert)

    return cert