# Схемы для пользователей
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Базовая схема для пользователя, содержащая основные поля.

    Attributes:
        username (str): Имя пользователя
        email (EmailStr): Email пользователя (автоматически валидируется как email)
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.

    Extends:
        UserBase: Наследует все поля из базовой схемы

    Attributes:
        username (str): Имя пользователя
        email (EmailStr): Email пользователя
        password (str): Пароль пользователя

    Note:
        Используется при регистрации нового пользователя
    """
    password: str


class User(UserBase):
    """
    Схема для существующего пользователя.

    Extends:
        UserBase: Наследует все поля из базовой схемы

    Attributes:
        id (int): Уникальный идентификатор пользователя
        username (str): Имя пользователя
        email (EmailStr): Email пользователя

    Note:
        Использует from_attributes для автоматического преобразования между Pydantic и SQLAlchemy моделями
    """
    id: int

    class Config:
        from_attributes = True
