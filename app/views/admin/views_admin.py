from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, Depends

from app.db.models import Product
from app.db.session import get_db


def get_list_product(db: Session = Depends(get_db)):
    print("Сработал get_list_product_wwww")
    try:
        # Используем text() для тестового запроса
        db.execute(text("SELECT 1"))
        print("Подключение к базе данных установлено успешно")

        products = db.query(Product).all()
        result = [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "store_id": p.store_id,
            "category_id": p.category_id
        } for p in products]
        print(f"result = {result}")
        return result
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных")