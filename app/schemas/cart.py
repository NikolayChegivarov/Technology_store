# Схемы для корзин.
from pydantic import BaseModel


class CartItemBase(BaseModel):
    """
    Базовая схема для элемента корзины, содержащая основные поля.

    Attributes:
        product_id (int): ID продукта в корзине
        quantity (int): Количество единиц продукта
    """
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    """
    Схема для создания нового элемента корзины.

    Extends:
        CartItemBase: Наследует все поля из базовой схемы

    Attributes:
        product_id (int): ID продукта для добавления в корзину
        quantity (int): Количество единиц продукта
    """
    pass


class CartItem(CartItemBase):
    """
    Схема для существующего элемента корзины.

    Extends:
        CartItemBase: Наследует все поля из базовой схемы

    Attributes:
        id (int): Уникальный идентификатор элемента корзины
        product_id (int): ID продукта в корзине
        quantity (int): Количество единиц продукта

    Note:
        Использует from_attributes для автоматического преобразования между Pydantic и SQLAlchemy моделями
    """
    id: int

    class Config:
        from_attributes = True
