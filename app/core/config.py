import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ACCESS_TOKEN_SECRET_KEY: str = os.getenv(
        "ACCESS_TOKEN_SECRET_KEY", "your_secret_key"
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)
    )  # 7 days
    REFRESH_TOKEN_SECRET_KEY: str = os.getenv(
        "REFRESH_TOKEN_SECRET_KEY", "your_refresh_secret_key"
    )
    PASSWORD_RESET_SECRET_KEY: str = os.getenv(
        "PASSWORD_RESET_SECRET_KEY", "your_password_reset_secret_key"
    )
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Boilerplate")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", False)
    DATABASE_URL: str = os.getenv("DATABASE_URL", None)
    BASE_API: str = os.getenv("BASE_API", "/api/v1")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))

    class Config:
        env_file = ".env"


settings = Settings()
