from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.models import Category
from app.schemas.category import CategoryCreate
from typing import List


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    """Получить категорию по ID"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Category]:
    """Получить список категорий с пагинацией"""
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


async def get_categories_with_products(db: AsyncSession) -> list[Category]:
    """Получить категории с загруженными продуктами"""
    result = await db.execute(
        select(Category).options(selectinload(Category.products))
    )
    return result.scalars().all()


async def create_category(db: AsyncSession, category: CategoryCreate) -> Category:
    """Создать новую категорию"""
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_categories(db: AsyncSession, category_ids: List[int]) -> int:
    """Удалить категории по списку ID"""
    count = 0
    for category_id in category_ids:
        category = await db.get(Category, category_id)
        if category:
            await db.delete(category)
            count += 1
    await db.commit()
    return count