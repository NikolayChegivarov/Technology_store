# Схемы для продуктов:
from pydantic import BaseModel
from typing import Optional
from app.schemas.store import Store
from app.schemas.category import Category


class ProductBase(BaseModel):
    """
    Базовая схема для продукта, содержащая основные поля.

    Attributes:
        name (str): Название продукта
        description (str): Описание продукта
        price (float): Цена продукта
        store_id: (int) Магазин
    """
    name: str
    description: str
    price: float
    store_id: int
    category_id: int


class ProductCreate(ProductBase):
    """
    Схема для создания нового продукта.

    Extends:
        ProductBase: Наследует все поля из базовой схемы

    Attributes:
        name (str): Название продукта
        description (str): Описание продукта
        price (float): Цена продукта
    """
    pass


class Product(ProductBase):
    """
    Схема для существующего продукта.

    Extends:
        ProductBase: Наследует все поля из базовой схемы

    Attributes:
        id (int): Уникальный идентификатор продукта
        name (str): Название продукта
        description (str): Описание продукта
        price (float): Цена продукта

    Note:
        Использует from_attributes для автоматического преобразования между Pydantic и SQLAlchemy моделями
    """
    id: int
    store: Store
    category: Optional[Category] = None

    class Config:
        from_attributes = True
