# Роутеры для аутентификации
from fastapi import APIRouter
from app.auth.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])