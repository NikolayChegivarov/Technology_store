# Роутеры для заказов
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.order import create_order, get_orders
from app.schemas.order import Order, OrderCreate

router = APIRouter()


@router.post("/", response_model=Order)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Создание нового заказа.

    Args:
        order (OrderCreate): Данные для создания нового заказа
        db (Session): Сессия базы данных для выполнения операций

    Returns:
        Order: Созданный заказ

    Raises:
        HTTPException: Если возникла ошибка при создании заказа
    """
    return create_order(db=db, order=order)


@router.get("/", response_model=list[Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка заказов с поддержкой пагинации.

    Args:
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)
        db (Session): Сессия базы данных для выполнения запросов

    Returns:
        list[Order]: Список объектов Order, содержащих информацию о заказах

    Raises:
        HTTPException: Если возникла ошибка при получении данных из базы данных
    """
    orders = get_orders(db, skip=skip, limit=limit)
    return orders
