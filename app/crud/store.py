# CRUD-операции для торговых точек
from sqlalchemy.orm import Session
from app.db.models import Store
from app.schemas.store import StoreCreate


def get_store(db: Session, store_id: int):
    """
    Получение информации о конкретном магазине по его ID.

    Args:
        db (Session): Сессия базы данных
        store_id (int): ID магазина для получения

    Returns:
        Store | None: Объект Store если найден, None если магазин не существует

    Note:
        Использует SQLAlchemy для точного поиска магазина по ID
    """
    return db.query(Store).filter(Store.id == store_id).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение списка магазинов с поддержкой пагинации.

    Args:
        db (Session): Сессия базы данных
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)

    Returns:
        list[Store]: Список объектов Store

    Note:
        Использует SQLAlchemy для эффективного запроса к базе данных
    """
    return db.query(Store).offset(skip).limit(limit).all()


def create_store(db: Session, store: StoreCreate):
    """
    Создание нового магазина.

    Args:
        db (Session): Сессия базы данных
        store (StoreCreate): Данные для создания нового магазина

    Returns:
        Store: Созданный магазин с заполненным ID

    Note:
        - Преобразует StoreCreate в Store
        - Сохраняет магазин в базе данных
        - Обновляет данные из базы данных
        - Возвращает полный объект с ID
    """
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store
