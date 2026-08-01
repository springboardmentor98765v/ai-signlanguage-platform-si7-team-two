from uuid import UUID
from services.notification_client import send_notification
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import SessionLocal
from models.assessment_model import Assessment
from models.practice_model import Certificate, Lesson, PracticeSession
from schemas.certificate_schema import (
    CertificateEligibilityResponse,
    CertificateIssuedResponse,
)
from services.certificate_engine import (
    check_certificate_eligibility,
    generate_certificate_code,
)
from services.certificate_generator import generate_certificate_pdf

router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/{learner_id}/eligibility",
    response_model=CertificateEligibilityResponse,
)
def check_eligibility(
    learner_id: UUID,
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == learner_id)
        .all()
    )

    session_ids = [s.id for s in sessions]

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .all()
        if session_ids
        else []
    )

    required_letters = [
        lesson.letter
        for lesson in db.query(Lesson).all()
        if lesson.letter
    ]

    result = check_certificate_eligibility(
        sessions,
        assessments,
        required_letters,
    )

    return {
        "learner_id": learner_id,
        **result,
    }


@router.post(
    "/{learner_id}/issue",
)
def issue_certificate(
    learner_id: UUID,
    learner_name: str,
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == learner_id)
        .all()
    )

    session_ids = [s.id for s in sessions]

    assessments = (
        db.query(Assessment)
        .filter(Assessment.session_id.in_(session_ids))
        .all()
        if session_ids
        else []
    )

    required_letters = [
        lesson.letter
        for lesson in db.query(Lesson).all()
        if lesson.letter
    ]

    result = check_certificate_eligibility(
        sessions,
        assessments,
        required_letters,
    )

    if not result["eligible"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Learner is not yet eligible for a certificate.",
                "missing_letters": result["missing_letters"],
                "average_score": result["average_score"],
            },
        )

    completed_sessions = [
        s for s in sessions
        if s.status == "completed"
    ]

    existing_certificate = (
        db.query(Certificate)
        .filter(
            Certificate.learner_id == learner_id,
            Certificate.is_valid == True,
        )
        .first()
    )

    # If certificate already exists, regenerate/download the PDF
    if existing_certificate:

        if existing_certificate.file_path:
            return FileResponse(
                path=existing_certificate.file_path,
                media_type="application/pdf",
                filename=f"Certificate_{learner_name}.pdf",
            )

        certificate_code = existing_certificate.certificate_code

    else:
        certificate_code = generate_certificate_code(learner_id)

        existing_certificate = Certificate(
            learner_id=learner_id,
            average_score=result["average_score"],
            lessons_completed=len(completed_sessions),
            certificate_code=certificate_code,
        )

        db.add(existing_certificate)
        db.commit()
        db.refresh(existing_certificate)

    file_path = generate_certificate_pdf(
        learner_name,
        result["average_score"],
        certificate_code,
    )

    existing_certificate.file_path = file_path
    db.commit()
    db.refresh(existing_certificate)

    send_notification(
        user_id=learner_id,
        title="Certificate Issued",
        message="Congratulations! You have earned your certificate. Click to download it.",
    )
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"Certificate_{learner_name}.pdf",
    )