# Роутеры для торговых точек
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.store import get_store, get_stores, create_store
from app.schemas.store import Store, StoreCreate

router = APIRouter()


@router.post("/", response_model=Store)
def create_new_store(store: StoreCreate, db: Session = Depends(get_db)):
    """
    Создание нового магазина.

    Args:
        store (StoreCreate): Данные для создания нового магазина
        db (Session): Сессия базы данных

    Returns:
        Store: Созданный магазин

    Raises:
        HTTPException: Если возникла ошибка при создании магазина
    """
    return create_store(db=db, store=store)


@router.get("/", response_model=list[Store])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка магазинов с поддержкой пагинации.

    Args:
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)
        db (Session): Сессия базы данных

    Returns:
        list[Store]: Список объектов Store

    Raises:
        HTTPException: Если возникла ошибка при получении данных из базы данных
    """
    stores = get_stores(db, skip=skip, limit=limit)
    return stores


@router.get("/{store_id}", response_model=Store)
def read_store(store_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о конкретном магазине по его ID.

    Args:
        store_id (int): ID магазина для получения
        db (Session): Сессия базы данных

    Returns:
        Store: Объект Store с информацией о магазине

    Raises:
        HTTPException: Если магазин с указанным ID не найден
    """
    db_store = get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store
