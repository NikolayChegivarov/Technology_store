# Функции, связанные с пользователями.
from sqlalchemy.orm import Session
from app.db.models import User


def get_user_by_username(db: Session, username: str):
    """
    Получение информации о пользователе по его username.

    Args:
        db (Session): Сессия базы данных
        username (str): Имя пользователя для поиска

    Returns:
        User | None: Объект User если найден, None если пользователь не существует

    Note:
        Использует SQLAlchemy для поиска пользователя по username
    """
    return db.query(User).filter(User.username == username).first()