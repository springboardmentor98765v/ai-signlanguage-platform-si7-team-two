from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import require_instructor
from app.schemas.instructor_schema import StudentProgressResponse, StudentResponse
from app.services.instructor_service import InstructorService

router = APIRouter()


@router.get("/students", response_model=List[StudentResponse])
def get_assigned_students(
    db: Session = Depends(get_db),
    current_user=Depends(require_instructor),
):
    return InstructorService.get_assigned_students(db)


@router.get("/student/{student_id}/progress", response_model=StudentProgressResponse)
def get_student_progress(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_instructor),
):
    return InstructorService.get_student_progress(
        db,
        student_id,
    )


@router.get("/student/{student_id}/assessments")
def get_student_assessments(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_instructor),
):
    return InstructorService.get_student_assessments(
        db,
        student_id,
    )
