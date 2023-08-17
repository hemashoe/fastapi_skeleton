from datetime import datetime, timedelta
from typing import Optional

from src.core.settings import variables
from jose import jwt
from passlib.context import CryptContext


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=variables.token_life)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, variables.secret_key, algorithm=variables.algorithm
    )
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
