from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.cache import (
    blacklist_token,
    clear_phone_verification_code,
    clear_refresh_token,
    is_token_blacklisted,
    set_email_verification_token,
    set_phone_verification_code,
    email_verification_token_exists,
    phone_verification_code_exists,
    set_refresh_token,
    is_refresh_token_valid,
    clear_email_verification_token,
)
from app.models.user import (
    UserCreate,
    UserLogin,
    Token,
    User,
    PasswordResetRequest,
    PasswordResetConfirm,
    EmailVerificationRequest,
    EmailVerificationConfirm,
    PhoneVerificationRequest,
    PhoneVerificationConfirm,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    refresh_access_token,
    create_password_reset_token,
    verify_password_reset_token,
    generate_email_token,
    generate_phone_code,
)

auth_router = APIRouter()


@auth_router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Hashes the password
    - Checks for duplicate email
    - Returns access and refresh tokens
    """
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user_in.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password", None))
    user = User.create(db, **user_data)
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    set_refresh_token(
        refresh_token, user.id, expires_minutes=60 * 24 * 7
    )  # 1 week default
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user.
    - Verifies password
    - Returns new access and refresh tokens
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    set_refresh_token(refresh_token, user.id, expires_minutes=60 * 24 * 7)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/refresh", response_model=Token)
def refresh_token(token_in: Token):
    """
    Refresh access and refresh tokens.
    - Checks if refresh token is valid and not revoked
    - Issues new tokens
    """
    if not is_refresh_token_valid(token_in.refresh_token):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = refresh_access_token(token_in.refresh_token)
    # Optional: rotate refresh token for added security
    # clear_refresh_token(token_in.refresh_token)
    # new_refresh = create_refresh_token(...)
    # set_refresh_token(new_refresh, ...)
    return {
        "access_token": access_token,
        "refresh_token": token_in.refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/logout")
def logout(token: Token):
    """
    Logout a user by blacklisting access and refresh tokens.
    """
    clear_refresh_token(token.refresh_token)
    blacklist_token(token.access_token)
    return {"message": "Logged out successfully."}


@auth_router.post("/request-password-reset")
def request_password_reset(
    request: PasswordResetRequest, db: Session = Depends(get_db)
):
    """
    Request a password reset.
    - Generates a time-limited password reset token
    - TODO: Email the token to the user
    - Does NOT reveal if the email exists for security
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return {
            "message": "If your email exists, you will receive a reset email shortly."
        }

    reset_token = create_password_reset_token(user.email)
    # TODO: Send reset_token via email
    return {"reset_token": reset_token}


@auth_router.post("/reset-password")
def reset_password(confirm: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Reset the user's password.
    - Checks the reset token
    - Hashes the new password and updates it
    """
    if is_token_blacklisted(confirm.token):
        raise HTTPException(status_code=400, detail="Token has been blacklisted")

    email = verify_password_reset_token(confirm.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    user.hashed_password = hash_password(confirm.new_password)
    db.commit()
    blacklist_token(confirm.token)  # Optionally blacklist the reset token
    return {"message": "Password has been reset successfully."}


@auth_router.post("/request-email-verification")
def request_email_verification(
    req: EmailVerificationRequest, db: Session = Depends(get_db)
):
    """
    Request an email verification.
    - Generates a verification token
    - Stores it in Redis
    - TODO: Email the token to the user
    """
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = generate_email_token()
    set_email_verification_token(token)
    # TODO: Send token via email
    return {"message": "Verification email sent.", "token": token}


@auth_router.post("/verify-email")
def verify_email(req: EmailVerificationConfirm, db: Session = Depends(get_db)):
    """
    Verify user's email.
    - Checks token validity from Redis
    - Marks email as verified and clears the token
    """
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not email_verification_token_exists(req.token):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.is_email_verified = True
    clear_email_verification_token(req.token)
    db.commit()
    return {"message": "Email verified."}


@auth_router.post("/request-phone-verification")
def request_phone_verification(
    req: PhoneVerificationRequest, db: Session = Depends(get_db)
):
    """
    Request a phone number verification.
    - Generates a code
    - Stores it in Redis
    - TODO: Send code via SMS to the user
    """
    user = db.query(User).filter(User.phone_number == req.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    code = generate_phone_code()
    set_phone_verification_code(user.phone_number, code)
    # TODO: Send code via SMS
    return {"message": "Verification code sent.", "code": code}


@auth_router.post("/verify-phone")
def verify_phone(req: PhoneVerificationConfirm, db: Session = Depends(get_db)):
    """
    Verify user's phone number.
    - Checks code validity from Redis
    - Marks phone as verified and clears the code
    """
    user = db.query(User).filter(User.phone_number == req.phone_number).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not phone_verification_code_exists(user.phone_number, req.code):
        raise HTTPException(status_code=400, detail="Invalid code")
    user.is_phone_verified = True
    clear_phone_verification_code(user.phone_number)
    db.commit()
    return {"message": "Phone number verified."}
