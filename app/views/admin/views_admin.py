from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, Depends

from app.db.models import Product
from app.db.session import get_db

from sqlalchemy.orm import selectinload


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
