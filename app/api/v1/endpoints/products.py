# Роутеры для товаров
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.product import get_products, get_product
from app.schemas.product import Product

router = APIRouter()


@router.get("/", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка продуктов с поддержкой пагинации.

    Args:
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)
        db (Session): Сессия базы данных для выполнения запросов

    Returns:
        list[Product]: Список объектов Product, содержащих информацию о продуктах

    Raises:
        HTTPException: Если возникла ошибка при получении данных из базы данных
    """
    products = get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о конкретном продукте по его ID.

    Args:
        product_id (int): ID продукта для получения информации
        db (Session): Сессия базы данных для выполнения запросов

    Returns:
        Product: Объект Product, содержащий детальную информацию о продукте

    Raises:
        HTTPException: Если продукт с указанным ID не найден
    """
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
