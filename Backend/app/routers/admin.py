from uuid import UUID
from fastapi import UploadFile, File
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import require_admin
from app.schemas.admin_schema import UserResponse
from app.services.admin_service import AdminService

router = APIRouter()

@router.post("/lessons/upload")
def upload_lessons_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    # current_user=Depends(require_admin),
):
    return AdminService.upload_lessons_csv(
    db,
    file,
)


@router.get(
    "/users",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return AdminService.get_all_users(db)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        return AdminService.delete_user(
            db,
            user_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post("/lessons/upload")
def upload_lessons_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return AdminService.upload_lessons_csv(
        db,
        file,
    )
