from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

from core.config import settings
from db.models import User
from .errors import NoSuchUserError
from .hashing import Hasher
from .users import get_user


def authenticate_user(username: str, pw: str, db: Session) -> bool | User:
    try:
        user = get_user(username, db)
    except NoSuchUserError:
        return False
    if not Hasher.verify_password(pw, user.hashedpw):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
