# CRUD-операции для корзины
from sqlalchemy.orm import Session
from app.db.models import CartItem
from app.schemas.cart import CartItemCreate


def add_to_cart(db: Session, cart_item: CartItemCreate):
    """
    Добавление нового элемента в корзину.

    Args:
        db (Session): Сессия базы данных
        cart_item (CartItemCreate): Данные для создания нового элемента корзины

    Returns:
        CartItem: Созданный элемент корзины с заполненным ID

    Note:
        - Преобразует CartItemCreate в CartItem
        - Сохраняет элемент в базе данных
        - Обновляет данные из базы данных
        - Возвращает полный объект с ID
    """
    db_cart_item = CartItem(**cart_item.dict())
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item


def get_cart_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение списка элементов корзины с поддержкой пагинации.

    Args:
        db (Session): Сессия базы данных
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)

    Returns:
        list[CartItem]: Список элементов корзины

    Note:
        - Использует SQLAlchemy для эффективного запроса к базе данных
        - Поддерживает пагинацию через параметры skip и limit
    """
    return db.query(CartItem).offset(skip).limit(limit).all()