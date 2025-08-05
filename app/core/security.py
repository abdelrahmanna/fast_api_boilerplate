from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: str | Any,
    expires_delta: timedelta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM]
        )
        subject = payload.get("sub")
        if subject is None:
            raise jwt.InvalidTokenError("Invalid refresh token")
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(subject, expires_delta)
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Refresh token has expired")
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"Invalid refresh token: {str(e)}")


def reusable_oauth2():
    return OAuth2PasswordBearer(tokenUrl=f"{settings.BASE_API}/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_password_reset_token(email: str, expires_minutes: int = 10):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": email, "exp": expire, "type": "reset"}
    return jwt.encode(
        to_encode, settings.PASSWORD_RESET_SECRET_KEY, algorithm=ALGORITHM
    )


def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.PASSWORD_RESET_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


import secrets
import random


def generate_email_token():
    return secrets.token_urlsafe(32)


def generate_phone_code():
    return str(random.randint(100000, 999999))
