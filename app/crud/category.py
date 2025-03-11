from sqlalchemy.orm import Session
from app.db.models import Category
from app.schemas.category import CategoryCreate


def get_category(db: Session, category_id: int):
    """
    Получение категории по ID.

    Args:
        db (Session): Сессия базы данных
        category_id (int): ID категории для поиска

    Returns:
        Category: Объект категории или None, если категория не найдена

    Note:
        Использует SQLAlchemy для выполнения запроса к базе данных
    """
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение списка категорий с возможностью постраничной загрузки.

    Args:
        db (Session): Сессия базы данных
        skip (int): Количество записей для пропуска (по умолчанию 0)
        limit (int): Максимальное количество записей для возврата (по умолчанию 100)

    Returns:
        List[Category]: Список объектов категорий

    Note:
        Использует SQLAlchemy для выполнения запроса с пагинацией
    """
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate):
    """
    Создание новой категории.

    Args:
        db (Session): Сессия базы данных
        category (CategoryCreate): Данные для создания категории

    Returns:
        Category: Созданный объект категории

    Note:
        Автоматически обновляет объект из базы данных после создания
    """
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
