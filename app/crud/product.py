# CRUD-операции для товаров
from app.schemas.product import ProductCreate
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, Depends

from app.db.models import Product
from app.db.session import get_db

from sqlalchemy.orm import selectinload


def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение списка продуктов с поддержкой пагинации.

    Args:
        db (Session): Сессия базы данных
        skip (int): Количество элементов для пропуска (по умолчанию 0)
        limit (int): Максимальное количество элементов для возврата (по умолчанию 100)

    Returns:
        list[Product]: Список объектов Product

    Note:
        Использует SQLAlchemy для эффективного запроса к базе данных с пагинацией
    """
    return db.query(Product).offset(skip).limit(limit).all()


def get_list_product(db: Session = Depends(get_db)):
    print("Сработал get_list_product")
    try:
        # Проверяем подключение к базе данных
        db.execute(text("SELECT 1"))
        print("Подключение к базе данных установлено успешно")

        # Загружаем продукты с магазинами и категориями одним запросом
        products = (
            db.query(Product)
            .options(
                selectinload(Product.store),
                selectinload(Product.category)
            )
            .all()
        )

        # Преобразуем результаты в список словарей
        result = [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "store_name": p.store.name if hasattr(p, 'store') else None,
            "category_name": p.category.name if hasattr(p, 'category') else None
        } for p in products]

        print(f"result = {result}")
        return result

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")


def get_product(db: Session, product_id: int):
    """
    Получение информации о конкретном продукте по его ID.

    Args:
        db (Session): Сессия базы данных
        product_id (int): ID продукта для получения

    Returns:
        Product | None: Объект Product если найден, None если продукт не существует

    Note:
        Использует SQLAlchemy для точного поиска продукта по ID
    """
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
