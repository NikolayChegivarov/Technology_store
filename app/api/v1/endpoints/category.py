from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.category import get_category, get_categories, create_category
from app.schemas.category import Category, CategoryCreate

router = APIRouter()


@router.post("/", response_model=Category)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Создание новой категории.

    Args:
        category (CategoryCreate): Данные для создания категории
        db (Session): Сессия базы данных (автоматически внедряется через Depends)

    Returns:
        Category: Созданная категория

    Note:
        - Автоматически валидирует входные данные через Pydantic
        - Преобразует ответ в JSON согласно модели Category
        - Использует асинхронное взаимодействие с базой данных
    """
    return create_category(db=db, category=category)


@router.get("/", response_model=list[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка категорий с возможностью постраничной загрузки.

    Args:
        skip (int): Количество записей для пропуска (по умолчанию 0)
        limit (int): Максимальное количество записей для возврата (по умолчанию 100)
        db (Session): Сессия базы данных (автоматически внедряется через Depends)

    Returns:
        list[Category]: Список категорий

    Note:
        - Поддерживает пагинацию через параметры skip и limit
        - Автоматически преобразует список объектов в JSON
        - Возвращает пустой список, если категории не найдены
    """
    categories = get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """
    Получение категории по ID.

    Args:
        category_id (int): ID категории для поиска
        db (Session): Сессия базы данных (автоматически внедряется через Depends)

    Returns:
        Category: Объект категории

    Raises:
        HTTPException: 404 если категория не найдена

    Note:
        - Валидирует существование категории
        - Автоматически преобразует объект в JSON
        - Генерирует корректную ошибку 404 при отсутствии категории
    """
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
