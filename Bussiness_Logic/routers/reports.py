"""
Reports Router — Milestone 4, Day 4.

Provides PDF and Excel download endpoints for:
- Learning Report
- Assessment Report
- Accuracy Report
- Certification Report

Existing Progress Report endpoints remain unchanged.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import SessionLocal

from models.practice_model import (
    PracticeSession,
    Certificate,
)

from models.assessment_model import Assessment

from services.report_service import (
    build_learning_report,
    build_assessment_report,
    build_accuracy_report,
    build_certification_report,
)

from services.report_pdf import (
    generate_learning_report_pdf,
    generate_assessment_report_pdf,
    generate_accuracy_report_pdf,
    generate_certification_report_pdf,
)

from services.report_excel import (
    generate_learning_report_excel,
    generate_assessment_report_excel,
    generate_accuracy_report_excel,
    generate_certification_report_excel,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# COMMON DATABASE HELPER
# ---------------------------------------------------------

def get_learner_data(
    user_id: UUID,
    db: Session,
):
    """
    Fetch all practice, assessment and certificate
    records belonging to the learner.
    """

    sessions = (
        db.query(PracticeSession)
        .filter(
            PracticeSession.user_id == user_id
        )
        .all()
    )

    session_ids = [
        session.id
        for session in sessions
    ]

    if session_ids:
        assessments = (
            db.query(Assessment)
            .filter(
                Assessment.session_id.in_(session_ids)
            )
            .all()
        )
    else:
        assessments = []

    certificates = (
        db.query(Certificate)
        .filter(
            Certificate.learner_id == user_id
        )
        .all()
    )

    return (
        sessions,
        assessments,
        certificates,
    )


# =========================================================
# LEARNING REPORT
# =========================================================

@router.get("/{user_id}/learning/pdf")
def get_learning_report_pdf(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_learning_report(
        sessions,
        assessments,
    )

    file_path = generate_learning_report_pdf(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"Learning_Report_{learner_name}.pdf",
    )


@router.get("/{user_id}/learning/excel")
def get_learning_report_excel(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_learning_report(
        sessions,
        assessments,
    )

    file_path = generate_learning_report_excel(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        filename=f"Learning_Report_{learner_name}.xlsx",
    )


# =========================================================
# ASSESSMENT REPORT
# =========================================================

@router.get("/{user_id}/assessment/pdf")
def get_assessment_report_pdf(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_assessment_report(
        assessments,
    )

    file_path = generate_assessment_report_pdf(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"Assessment_Report_{learner_name}.pdf",
    )


@router.get("/{user_id}/assessment/excel")
def get_assessment_report_excel(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_assessment_report(
        assessments,
    )

    file_path = generate_assessment_report_excel(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        filename=f"Assessment_Report_{learner_name}.xlsx",
    )


# =========================================================
# ACCURACY REPORT
# =========================================================

@router.get("/{user_id}/accuracy/pdf")
def get_accuracy_report_pdf(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_accuracy_report(
        assessments,
    )

    file_path = generate_accuracy_report_pdf(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"Accuracy_Report_{learner_name}.pdf",
    )


@router.get("/{user_id}/accuracy/excel")
def get_accuracy_report_excel(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_accuracy_report(
        assessments,
    )

    file_path = generate_accuracy_report_excel(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        filename=f"Accuracy_Report_{learner_name}.xlsx",
    )


# =========================================================
# CERTIFICATION REPORT
# =========================================================

@router.get("/{user_id}/certification/pdf")
def get_certification_report_pdf(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_certification_report(
        certificates,
    )

    file_path = generate_certification_report_pdf(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=(
            f"Certification_Report_{learner_name}.pdf"
        ),
    )


@router.get("/{user_id}/certification/excel")
def get_certification_report_excel(
    user_id: UUID,
    learner_name: str = Query("Learner"),
    db: Session = Depends(get_db),
):

    sessions, assessments, certificates = (
        get_learner_data(user_id, db)
    )

    report_data = build_certification_report(
        certificates,
    )

    file_path = generate_certification_report_excel(
        learner_name=learner_name,
        report_data=report_data,
        user_id=str(user_id),
    )

    return FileResponse(
        path=file_path,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        filename=(
            f"Certification_Report_{learner_name}.xlsx"
        ),
    )