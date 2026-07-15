from fastapi import APIRouter
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.user_service import register_user, login_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register(user: UserRegister):
    return register_user(user)


@router.post("/login")
def login(user: UserLogin):
    return login_user(user)