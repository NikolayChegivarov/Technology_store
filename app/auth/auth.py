# Логика аутентификации
from datetime import timedelta  #
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.security import verify_password, create_access_token
from app.schemas.auth import Token
from app.utils.user_utils import get_user_by_username

# Константа для времени жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Добавляем константу

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Получение токена доступа через OAuth2 Password Flow.

    Args:
        form_data (OAuth2PasswordRequestForm): Форма с данными для аутентификации
        db (Session): Сессия базы данных

    Returns:
        Token: Объект содержащий токен доступа и его тип

    Raises:
        HTTPException: Если:
            - Неправильное имя пользователя или пароль
            - Ошибка аутентификации

    Note:
        - Использует OAuth2 Password Flow для аутентификации
        - Возвращает bearer-токен с указанным временем жизни
        - Включает username в payload токена
    """
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # для создания временного интервала, который
    access_token = create_access_token(                                 # определяет, как долго будет действовать токен.
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
