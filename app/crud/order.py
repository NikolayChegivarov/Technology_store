# CRUD-операции для заказов
from sqlalchemy.orm import Session
from app.db.models import Order
from app.schemas.order import OrderCreate


def create_order(db: Session, order: OrderCreate):
    """
    Создание нового заказа.

    Args:
        db (Session): Сессия базы данных
        order (OrderCreate): Данные для создания нового заказа

    Returns:
        Order: Созданный заказ с заполненным ID

    Note:
        - Преобразует OrderCreate в Order
        - Сохраняет заказ в базе данных
        - Обновляет данные из базы данных
        - Возвращает полный объект с ID
    """
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение списка заказов с поддержкой пагинации.

    Args:
        db (Session): Сессия базы данных
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)

    Returns:
        list[Order]: Список заказов

    Note:
        - Использует SQLAlchemy для эффективного запроса к базе данных
        - Поддерживает пагинацию через параметры skip и limit
    """
    return db.query(Order).offset(skip).limit(limit).all()
