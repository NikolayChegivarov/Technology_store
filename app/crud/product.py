# CRUD-операции для товаров
from app.schemas.product import ProductCreate
from sqlalchemy import select
from sqlalchemy import text
from fastapi import HTTPException, Depends, status

from app.db.models import Product
from app.db.session import get_db

from sqlalchemy.orm import selectinload

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
    """
    Получение списка продуктов с поддержкой пагинации.

    Args:
        db (AsyncSession): Асинхронная сессия базы данных
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)

    Returns:
        list[Product]: Список объектов Product

    Note:
        Использует SQLAlchemy для эффективного запроса к базе данных с пагинацией
    """
    return await db.query(Product).offset(skip).limit(limit).all()


async def get_product(db: AsyncSession, product_id: int) -> Product | None:
    """
    Получение информации о конкретном продукте по его ID.

    Args:
        db (AsyncSession): Асинхронная сессия базы данных
        product_id (int): ID продукта для получения

    Returns:
        Product | None: Объект Product если найден, None если продукт не существует

    Note:
        Использует SQLAlchemy для точного поиска продукта по ID
    """
    result = await db.query(Product).filter(Product.id == product_id).first()
    return result


async def get_list_product(db: AsyncSession = Depends(get_db)):
    print("Сработал get_list_product")
    try:
        await db.execute(text("SELECT 1"))
        print("Подключение к базе данных установлено успешно")

        # Используем новый стиль запросов с select
        stmt = select(Product).options(
            selectinload(Product.store),
            selectinload(Product.category)
        )
        result = await db.execute(stmt)
        products = result.scalars().all()

        # Формируем результат
        result = [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "store_name": p.store.name if p.store else None,
            "category_name": p.category.name if p.category else None
        } for p in products]

        print(f"result = {result}")
        return result

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")


async def create_product(db: AsyncSession, product: ProductCreate) -> Product:
    """
    Создание нового продукта в базе данных.

    Args:
        db (AsyncSession): Асинхронная сессия базы данных
        product (ProductCreate): Данные для создания продукта

    Returns:
        Product: Созданный продукт

    Note:
        Использует SQLAlchemy для создания записи в базе данных
    """
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_selected(product_ids: List[int], session: AsyncSession):
    """Удаляет продукты по списку ID"""
    if not product_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не выбраны товары для удаления"
        )

    await session.execute(
        delete(Product).where(Product.id.in_(product_ids))
    )
    await session.commit()


