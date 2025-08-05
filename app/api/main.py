from fastapi import APIRouter

from app.core.config import settings
from app.api.routes.user import user_router
from app.api.routes.auth import auth_router

api_router = APIRouter()


api_router.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)

if settings.ENVIRONMENT == "local":
    pass
