# CRUD-операции для товаров
from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.product import ProductCreate


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
