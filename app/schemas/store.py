# Схемы для торговых точек
from pydantic import BaseModel


class StoreBase(BaseModel):
    """
    Базовая схема для магазина, содержащая основные поля.

    Attributes:
        name (str): Название магазина
        address (str): Адрес магазина
    """
    name: str
    address: str
    city: str


class StoreCreate(StoreBase):
    """
    Схема для создания нового магазина.

    Extends:
        StoreBase: Наследует все поля из базовой схемы

    Attributes:
        name (str): Название магазина
        address (str): Адрес магазина

    Note:
        Используется при создании нового магазина
    """
    pass


class Store(StoreBase):
    """
    Схема для существующего магазина.

    Extends:
        StoreBase: Наследует все поля из базовой схемы

    Attributes:
        id (int): Уникальный идентификатор магазина
        name (str): Название магазина
        address (str): Адрес магазина

    Note:
        Использует from_attributes для автоматического преобразования между Pydantic и SQLAlchemy моделями
    """
    id: int

    class Config:
        from_attributes = True
