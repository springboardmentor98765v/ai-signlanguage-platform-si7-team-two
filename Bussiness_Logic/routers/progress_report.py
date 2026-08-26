from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.practice_model import PracticeSession
from models.assessment_model import Assessment
from models.practice_model import Certificate
from services.progress_report_engine import build_progress_report
from services.progress_report_pdf import generate_progress_report_pdf
from schemas.progress_report_schema import ProgressReportResponse
from datetime import datetime
from uuid import UUID
from fastapi.responses import FileResponse
from services.progress_report_excel import (
    generate_progress_report_excel,
    generate_instructor_summary_excel,
)
from models.practice_model import User
router = APIRouter(prefix="/progress-report", tags=["Progress Report Service"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/instructor/excel")
def export_instructor_summary(
    db: Session = Depends(get_db),
):
    learners = db.query(User).all()

    report_rows = []

    for learner in learners:

        sessions = db.query(PracticeSession).filter(
            PracticeSession.user_id == learner.id
        ).all()

        if not sessions:
            continue

        session_ids = [session.id for session in sessions]

        assessments = db.query(Assessment).filter(
            Assessment.session_id.in_(session_ids)
        ).all()

        certificates = db.query(Certificate).filter(
            Certificate.learner_id == learner.id
        ).all()

        report = build_progress_report(
            sessions,
            assessments,
            certificates,
        )

        report_rows.append({
            "user_id": str(learner.id),
            "lessons_completed": report["lessons_completed"],
            "average_accuracy": report["average_accuracy"],
            "total_attempts": report["total_attempts"],
            "certificates_earned": len(report["certificates_earned"]),
        })

    file_path = generate_instructor_summary_excel(report_rows)

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="Instructor_Summary.xlsx",
    )

@router.get("/{user_id}", response_model=ProgressReportResponse)
def get_progress_report(user_id: UUID, db: Session = Depends(get_db)):
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == user_id).all()
    session_ids = [s.id for s in sessions] if sessions else []
    assessments = db.query(Assessment).filter(Assessment.session_id.in_(session_ids)).all() if session_ids else []
    certificates = db.query(Certificate).filter(Certificate.learner_id == user_id).all()

    report_data = build_progress_report(sessions, assessments, certificates)

    return ProgressReportResponse(
        user_id=user_id,
        lessons_completed=report_data["lessons_completed"],
        total_practice_time=report_data["total_practice_time"],
        average_accuracy=report_data["average_accuracy"],
        attempted_letters=report_data["attempted_letters"],
        weak_letters=report_data["weak_letters"],
        total_attempts=report_data["total_attempts"],
        certificates_earned=report_data["certificates_earned"],
        generated_at=datetime.utcnow()
    )

@router.get("/{user_id}/pdf")
def get_progress_report_pdf(user_id: UUID, learner_name: str = Query("Learner"), db: Session = Depends(get_db)):
    sessions = db.query(PracticeSession).filter(PracticeSession.user_id == user_id).all()
    session_ids = [s.id for s in sessions] if sessions else []
    assessments = db.query(Assessment).filter(Assessment.session_id.in_(session_ids)).all() if session_ids else []
    certificates = db.query(Certificate).filter(Certificate.learner_id == user_id).all()

    report_data = build_progress_report(sessions, assessments, certificates)
    file_path = generate_progress_report_pdf(
        learner_name,
        report_data,
        str(user_id)
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"Progress_Report_{learner_name}.pdf",
    )

@router.get("/{user_id}/excel")
def get_progress_report_excel(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id
    ).all()

    session_ids = [session.id for session in sessions] if sessions else []

    assessments = db.query(Assessment).filter(
        Assessment.session_id.in_(session_ids)
    ).all() if session_ids else []

    certificates = db.query(Certificate).filter(
        Certificate.learner_id == user_id
    ).all()

    report_data = build_progress_report(
        sessions,
        assessments,
        certificates,
    )

    file_path = generate_progress_report_excel(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"Progress_Report_{learner_name}.xlsx",
    )
