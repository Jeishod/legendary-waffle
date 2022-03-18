from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from django.conf import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from data.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.EXPIRE_TOKEN)
    payload = {"user_id": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(claims=payload, key=settings.SECRET_KEY, algorithm=settings.PWD_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    data = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.PWD_ALGORITHM)
    return data


def authenticate(email: EmailStr, password: str) -> Optional[User]:
    db_user = await User.objects.get(email=email)
    if not db_user or not verify_password(plain_password=password, hashed_password=db_user.hashed_password):
        return None
    return db_user
