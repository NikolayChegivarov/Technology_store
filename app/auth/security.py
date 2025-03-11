# Логика безопасности (хеширование паролей, JWT)
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


from app.schemas.auth import TokenData
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.core.config import settings
from app.utils.user_utils import get_user_by_username

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    Проверка соответствия пароля его хешированной версии.

    Args:
        plain_password (str): Пароль в открытом виде
        hashed_password (str): Хешированная версия пароля

    Returns:
        bool: True если пароль верный, False если нет

    Note:
        Использует контекст хеширования для безопасной проверки пароля
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Создание хешированной версии пароля.

    Args:
        password (str): Пароль для хеширования

    Returns:
        str: Хешированная версия пароля

    Note:
        Использует алгоритм bcrypt для безопасного хеширования
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Создание JWT токена доступа.

    Args:
        data (dict): Данные для включения в токен
        expires_delta (timedelta | None): Время жизни токена

    Returns:
        str: JWT токен

    Note:
        - Добавляет время истечения срока действия
        - Использует SECRET_KEY для подписи
        - По умолчанию токен живет 15 минут
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Получение текущего пользователя из токена.

    Args:
        token (str): JWT токен доступа
        db (Session): Сессия базы данных

    Returns:
        User: Объект пользователя

    Raises:
        HTTPException: Если:
            - Токен недействителен
            - Токен истек
            - Пользователь не найден
            - Неверные учетные данные

    Note:
        - Проверяет валидность токена
        - Находит пользователя по username из токена
        - Использует OAuth2 схему аутентификации
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
