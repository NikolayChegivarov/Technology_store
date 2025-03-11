# Роутеры для корзины
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.cart import add_to_cart, get_cart_items
from app.schemas.cart import CartItem, CartItemCreate

router = APIRouter()


@router.post("/", response_model=CartItem)  # post запрос. Ответ будет форматирован согласно модели CartItem
def add_item_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):  # модель, подключение к db
    """Добавляет товар в корзину пользователя.

    Args:
        cart_item (CartItemCreate): Объект содержащий данные о добавляемом товаре
        db (Session): Сессия базы данных для выполнения операций с БД

    Returns:
        CartItem: Объект содержащий информацию о добавленном товаре в корзине

    Raises:
        HTTPException: Если возникла ошибка при добавлении товара в корзину
    """
    return add_to_cart(db=db, cart_item=cart_item)


@router.get("/", response_model=list[CartItem])  # get запрос. Ответом будет список объектов типа CartItem
def read_cart_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка товаров из корзины с поддержкой пагинации.

    Args:
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)
        db (Session): Сессия базы данных для выполнения запросов

    Returns:
        list[CartItem]: Список объектов CartItem, содержащих информацию о товарах в корзине

    Raises:
        HTTPException: Если возникла ошибка при получении данных из базы данных
    """
    cart_items = get_cart_items(db, skip=skip, limit=limit)
    return cart_items


