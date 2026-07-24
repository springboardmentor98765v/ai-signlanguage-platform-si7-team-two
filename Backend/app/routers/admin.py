from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from app.schemas.admin_schema import UserResponse
from app.services.admin_service import AdminService

router = APIRouter()


@router.get(
    "/users",
    response_model=list[UserResponse],
)
def get_users(db: Session = Depends(get_db)):
    return AdminService.get_all_users(db)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
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