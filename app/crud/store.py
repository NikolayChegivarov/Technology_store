# CRUD-операции для торговых точек
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Store
from app.schemas.store import StoreCreate


async def get_store(db: AsyncSession, store_id: int):
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
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    return result.scalars().first()


async def get_stores(db: AsyncSession, skip: int = 0, limit: int = 100):
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
    result = await db.execute(
        select(Store).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_list_stores(db: AsyncSession):
    """
    Получение списка всех магазинов (асинхронная версия).

    Args:
        db (AsyncSession): Асинхронная сессия базы данных

    Returns:
        List[Store]: Список всех магазинов
    """
    result = await db.execute(
        select(Store).options(selectinload(Store.products))
    )
    return result.scalars().all()


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


async def delete_store(db: AsyncSession, store_id: int):
    """
    Удаление магазина по ID (асинхронная версия).

    Args:
        db (AsyncSession): Асинхронная сессия базы данных
        store_id (int): ID магазина для удаления

    Returns:
        bool: True если магазин был удален, False если не найден
    """
    store = await db.get(Store, store_id)
    if store:
        await db.delete(store)
        await db.commit()
        return True
    return False


async def delete_stores(db: AsyncSession, store_ids: List[int]):
    """
    Удаление нескольких магазинов по списку ID (асинхронная версия).

    Args:
        db (AsyncSession): Асинхронная сессия базы данных
        store_ids (List[int]): Список ID магазинов для удаления

    Returns:
        int: Количество удаленных магазинов
    """
    count = 0
    for store_id in store_ids:
        store = await db.get(Store, store_id)
        if store:
            await db.delete(store)
            count += 1
    await db.commit()
    return count
