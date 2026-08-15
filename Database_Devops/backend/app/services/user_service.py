    from app.schemas.user_schema import UserRegister, UserLogin


    def register_user(user: UserRegister):
        return {
            "message": "User registered successfully",
            "user": {
                "full_name": user.full_name,
                "email": user.email
            }
        }


    def login_user(user: UserLogin):
        return {
            "message": "Login successful",
            "email": user.email
        }