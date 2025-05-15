from pydantic import BaseModel


class CategoryBase(BaseModel):
    """
    Базовая схема категории.

    Attributes:
        name (str): Название категории

    Note:
        Содержит основные поля для всех моделей категорий
    """
    name: str


class CategoryCreate(CategoryBase):
    """
    Схема для создания новой категории.

    Extends:
        CategoryBase: Наследует все поля из базовой схемы

    Attributes:
        name (str): Название категории для создания

    Note:
        Используется при POST-запросах для валидации входных данных
    """
    name: str


class Category(CategoryBase):
    """
    Схема существующей категории.

    Extends:
        CategoryBase: Наследует все поля из базовой схемы

    Attributes:
        id (int): Уникальный идентификатор категории
        name (str): Название категории

    Note:
        Использует from_attributes для автоматического преобразования между Pydantic и SQLAlchemy моделями
    """
    id: int

    class Config:
        from_attributes = True
