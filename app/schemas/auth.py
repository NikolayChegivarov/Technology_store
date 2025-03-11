# Схемы для аутентификации
from pydantic import BaseModel


class Token(BaseModel):
    """
    Схема для токена доступа.

    Attributes:
        access_token (str): Строка токена доступа
        token_type (str): Тип токена (например, "bearer")
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Схема для данных, извлекаемых из токена.

    Attributes:
        username (str | None): Имя пользователя из токена (может быть None)
    """
    username: str | None = None
