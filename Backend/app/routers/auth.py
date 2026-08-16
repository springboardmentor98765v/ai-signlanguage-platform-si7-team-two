from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    UpdateProfile,
    ChangePassword,
    ForgotPassword,
    ResetPassword,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        return AuthService.register(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        login_data = AuthService.login(db, user)

        logged_user = login_data["user"]
        role_name = login_data.get("role_name", "learner")

        return {
            "message": "Login successful",
            "access_token": login_data["access_token"],
            "token_type": login_data["token_type"],
            "user": {
                "id": str(logged_user.id),
                "full_name": logged_user.full_name,
                "email": logged_user.email,
                "role": role_name,
                "role_id": str(logged_user.role_id),
                "mascot_id": logged_user.mascot_id or "owl",
            },
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/user/{user_id}")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Fetch fresh user data from DB — used after refresh to avoid stale localStorage."""
    user = AuthService.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    role_name = user.role.name.lower() if user.role else "learner"
    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "role": role_name,
        "role_id": str(user.role_id),
        "mascot_id": user.mascot_id or "owl",
    }


@router.put("/profile/{user_id}", response_model=UserResponse)
def update_profile(
    user_id: str,
    profile: UpdateProfile,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.update_profile(
            db,
            user_id,
            profile,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/change-password/{user_id}")
def change_password(
    user_id: str,
    password_data: ChangePassword,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.change_password(
            db,
            user_id,
            password_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPassword,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.forgot_password(
            db,
            request.email,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post("/reset-password/{user_id}")
def reset_password(
    user_id: str,
    password_data: ResetPassword,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.reset_password(
            db,
            user_id,
            password_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


print("AUTH MODULE IMPORTED")
