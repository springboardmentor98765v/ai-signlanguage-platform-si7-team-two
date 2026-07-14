from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.database.database import get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        return AuthService.register(db, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        logged_user = AuthService.login(db, user)

        return {
            "message": "Login successful",
            "user": {
                "id": str(logged_user.id),
                "full_name": logged_user.full_name,
                "email": logged_user.email,
                "role_id": str(logged_user.role_id),
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


print("AUTH MODULE IMPORTED")
