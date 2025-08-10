from redis import Redis
from app.core.config import settings

r = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def blacklist_token(token: str, expires_seconds: int = 3600):
    r.set(f"blacklist:{token}", "true", ex=expires_seconds)


def is_token_blacklisted(token: str) -> bool:
    return r.exists(f"blacklist:{token}") > 0


def set_email_verification_token(token: str, expires_seconds: int = 3600):
    r.set(f"email_verification:{token}", "true", ex=expires_seconds)


def email_verification_token_exists(token: str) -> bool:
    return r.exists(f"email_verification:{token}") > 0


def clear_email_verification_token(token: str):
    r.delete(f"email_verification:{token}")


def set_phone_verification_code(
    phone_number: str, code: str, expires_seconds: int = 300
):
    r.set(f"phone_verification:{phone_number}", code, ex=expires_seconds)


def phone_verification_code_exists(phone_number: str, code: str) -> bool:
    return r.get(f"phone_verification:{phone_number}") == code


def clear_phone_verification_code(phone_number: str):
    r.delete(f"phone_verification:{phone_number}")


def set_refresh_token(token: str, user_id: int, expires_minutes: int):
    r.set(f"refresh_token:{token}", user_id, ex=expires_minutes * 60)


def is_refresh_token_valid(token: str) -> bool:
    return r.exists(f"refresh_token:{token}") > 0


def clear_refresh_token(token: str):
    r.delete(f"refresh_token:{token}")
