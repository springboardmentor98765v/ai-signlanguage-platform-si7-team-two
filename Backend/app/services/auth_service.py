from sqlalchemy.orm import Session
from uuid import UUID

from sqlalchemy import select

from app.models.user import User
from app.models.role import Role

from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UpdateProfile,
    ChangePassword,
    ResetPassword,
)


class AuthService:
    @staticmethod
    def register(db: Session, user: UserRegister):
        try:
            print("Register called")
            print("Requested role:", user.role)

            # Check whether email already exists
            existing_user = db.execute(
                select(User).where(User.email == user.email)
            ).scalar_one_or_none()

            if existing_user is not None:
                raise ValueError("Email already registered")

            # Find the selected role from the database
            selected_role = db.execute(
                select(Role).where(Role.name.ilike(user.role))
            ).scalar_one_or_none()

            print("Selected role:", selected_role)

            if selected_role is None:
                raise ValueError(
                    f"Role '{user.role}' does not exist in the database."
                )

            # Hash password
            print("Hashing password...")
            hashed = hash_password(user.password)
            print("Password hashed successfully")

            # Create user with the SELECTED role
            new_user = User(
                full_name=user.full_name,
                email=user.email,
                password_hash=hashed,
                role_id=selected_role.id,
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            print(
                "User created:",
                new_user.id,
                "Role:",
                selected_role.name,
            )

            return new_user

        except ValueError:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            print("REGISTER ERROR:", repr(e))
            raise
    @staticmethod
    def login(db: Session, user: UserLogin):

        existing_user = db.execute(
            select(User).where(User.email == user.email)
        ).scalar_one_or_none()

        if existing_user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(
            user.password,
            existing_user.password_hash,
        ):
            raise ValueError("Invalid email or password")

        # Load the role name via relationship
        role_name = (
            existing_user.role.name.strip().lower()
            if existing_user.role
            else "learner"
        )

        token = create_access_token(
            {
                "sub": str(existing_user.id),
                "email": existing_user.email,
                "role": role_name,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": existing_user,
            "role_name": role_name,
        }

    @staticmethod
    def get_user(db: Session, user_id: str):
        return db.execute(
            select(User).where(User.id == UUID(str(user_id)))
        ).scalar_one_or_none()

    @staticmethod
    def update_profile(
        db: Session,
        user_id,
        profile: UpdateProfile,
    ):
        existing_user = db.execute(
            select(User).where(User.id == UUID(str(user_id)))
        ).scalar_one_or_none()

        if existing_user is None:
            raise ValueError("User not found")

        existing_user.full_name = profile.full_name
        existing_user.email = profile.email

        # Persist mascot selection so it survives refresh / logout
        if profile.mascot_id is not None:
            existing_user.mascot_id = profile.mascot_id

        db.commit()
        db.refresh(existing_user)

        return existing_user

    @staticmethod
    def change_password(
        db: Session,
        user_id,
        password_data: ChangePassword,
    ):
        existing_user = db.execute(
            select(User).where(User.id == UUID(str(user_id)))
        ).scalar_one_or_none()

        if existing_user is None:
            raise ValueError("User not found")

        if not verify_password(
            password_data.old_password,
            existing_user.password_hash,
        ):
            raise ValueError("Old password is incorrect")

        existing_user.password_hash = hash_password(password_data.new_password)
        db.commit()

        return {"message": "Password changed successfully"}

    @staticmethod
    def forgot_password(
        db: Session,
        email: str,
    ):
        existing_user = db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

        if existing_user is None:
            raise ValueError("Email not found")

        reset_link = f"http://localhost:8000/reset-password/{existing_user.id}"

        return {
            "message": "Password reset link generated successfully.",
            "reset_link": reset_link,
        }

    @staticmethod
    def reset_password(
        db: Session,
        user_id,
        password_data: ResetPassword,
    ):
        existing_user = db.execute(
            select(User).where(User.id == UUID(str(user_id)))
        ).scalar_one_or_none()

        if existing_user is None:
            raise ValueError("User not found")

        existing_user.password_hash = hash_password(password_data.new_password)
        db.commit()

        return {"message": "Password reset successfully"}
