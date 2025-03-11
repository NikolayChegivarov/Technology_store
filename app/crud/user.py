# CRUD-операции для пользователей
from sqlalchemy.orm import Session

from app.auth.security import get_password_hash
from app.db.models import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    """
    Получение информации о пользователе по его ID.

    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя для поиска

    Returns:
        User | None: Объект User если найден, None если пользователь не существует

    Note:
        Использует SQLAlchemy для точного поиска пользователя по ID
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    """
    Создание нового пользователя с хешированным паролем.

    Args:
        db (Session): Сессия базы данных
        user (UserCreate): Данные для создания нового пользователя

    Returns:
        User: Созданный пользователь с заполненным ID

    Note:
        - Хеширует пароль перед сохранением
        - Сохраняет пользователя в базе данных
        - Обновляет данные из базы данных
        - Возвращает полный объект с ID
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    """
    Получение информации о пользователе по его email.

    Args:
        db (Session): Сессия базы данных
        email (str): Email пользователя для поиска

    Returns:
        User | None: Объект User если найден, None если пользователь не существует

    Note:
        Использует SQLAlchemy для поиска пользователя по email
    """
    return db.query(User).filter(User.email == email).first()
