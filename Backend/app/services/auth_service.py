from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models.users import User
from db.models.roles import Role

from app.utils.hashing import hash_password, verify_password
from app.schemas.user import UserRegister, UserLogin


class AuthService:

    @staticmethod
    def register(db: Session, user: UserRegister):
        # Check if email already exists
        existing_user = db.execute(
            select(User).where(User.email == user.email)
        ).scalar_one_or_none()

        if existing_user:
            raise ValueError("Email already registered")

        # Get Learner role
        learner_role = db.execute(
            select(Role).where(Role.name == "Learner")
        ).scalar_one_or_none()

        if learner_role is None:
            raise ValueError("Learner role not found")

        # Create user
        new_user = User(
            full_name=user.full_name,
            email=user.email,
            password_hash=hash_password(user.password),
            role_id=learner_role.id,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def login(db: Session, user: UserLogin):

        existing_user = db.execute(
            select(User).where(User.email == user.email)
        ).scalar_one_or_none()

        if existing_user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(
            user.password,
            existing_user.password_hash
        ):
            raise ValueError("Invalid email or password")

        return existing_user