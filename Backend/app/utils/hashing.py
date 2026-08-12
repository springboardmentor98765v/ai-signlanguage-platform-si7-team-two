from passlib.context import CryptContext
import traceback

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    try:
        print("Inside hash_password")
        hashed = pwd_context.hash(password)
        print("Hash created:", hashed[:20])
        return hashed
    except Exception as e:
        print("HASH ERROR:", repr(e))
        traceback.print_exc()
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
