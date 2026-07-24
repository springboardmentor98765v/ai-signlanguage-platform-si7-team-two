from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.instructor_schema import StudentResponse
from app.database.database import get_db
from app.services.instructor_service import InstructorService

router = APIRouter()


@router.get("/students", response_model=List[StudentResponse])
def get_assigned_students(
    db: Session = Depends(get_db),
):
    return InstructorService.get_assigned_students(db)


@router.get("/student/{student_id}/progress")
def get_student_progress(
    student_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return InstructorService.get_student_progress(
            db,
            student_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/student/{student_id}/assessments")
def get_student_assessments(
    student_id: UUID,
    db: Session = Depends(get_db),
):
    return InstructorService.get_student_assessments(
        db,
        student_id,
    )