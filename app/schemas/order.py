# Схемы для заказов
from pydantic import BaseModel


class OrderBase(BaseModel):
    """
    Базовая схема для заказа, содержащая основные поля.

    Attributes:
        user_id (int): ID пользователя, который создал заказ
        total_price (float): Общая стоимость заказа
    """
    user_id: int
    total_price: float


class OrderCreate(OrderBase):
    """
    Схема для создания нового заказа.

    Extends:
        OrderBase: Наследует все поля из базовой схемы

    Attributes:
        user_id (int): ID пользователя, который создает заказ
        total_price (float): Общая стоимость заказа
    """
    pass


class Order(OrderBase):
    """
    Схема для существующего заказа.

    Extends:
        OrderBase: Наследует все поля из базовой схемы

    Attributes:
        id (int): Уникальный идентификатор заказа
        user_id (int): ID пользователя, который создал заказ
        total_price (float): Общая стоимость заказа

    Note:
        Использует from_attributes  для автоматического преобразования между Pydantic и SQLAlchemy моделями
    """
    id: int

    class Config:
        from_attributes = True
