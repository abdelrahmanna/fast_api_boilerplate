"""
Pydantic schemas for the User entity.
"""

from sqlalchemy import Boolean, Column, Integer, String
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.base import Base
from app.db.mixins import TimestampMixin, CRUDMixin, SoftDeleteMixin


class UserBase(BaseModel):
    """
    Shared attributes for all operations with User.
    """

    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_email_verified: bool = False
    is_phone_verified: bool = False
    phone_number: Optional[str] = None
    is_active: bool = True

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """
    Schema for creating a new User.
    """

    password: str


class UserUpdate(BaseModel):
    """
    Schema for updating an existing User.
    """

    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_email_verified: bool = False
    is_phone_verified: bool = False
    phone_number: Optional[str] = None
    is_active: bool = True


class UserOut(UserBase):
    """
    Schema for reading a User with ID.
    """

    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    email: str
    token: str


class PhoneVerificationRequest(BaseModel):
    phone_number: str


class PhoneVerificationConfirm(BaseModel):
    phone_number: str
    code: str


"""
SQLAlchemy model definition for the User entity.
"""


class User(Base, TimestampMixin, CRUDMixin, SoftDeleteMixin):
    """
    SQLAlchemy model for the User table.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class TokenPayload(BaseModel):
    """
    Payload for JWT token.
    """

    sub: str
    exp: Optional[int] = None

    class Config:
        orm_mode = True
