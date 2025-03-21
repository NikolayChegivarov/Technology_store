# Точка входа в приложение, где создается экземпляр FastAPI и подключаются роутеры.
# from urllib import request
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from app.api.v1.endpoints import products, cart, orders, users, auth, stores, category
from app.crud.product import get_list_product, delete_selected, create_product
from app.db.models import Store, Category
from app.db.session import get_db
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import Form
from sqlalchemy.future import select
from starlette.middleware.sessions import SessionMiddleware
import os

from app.schemas.product import ProductCreate

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")

# Подключите SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Подключаем статические файлы из папки frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Подключаем роутеры API
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["cart"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(stores.router, prefix="/api/v1/stores", tags=["stores"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["categories"])


# Редирект с корневого пути на index.html
@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")  # Перенаправляем на index.html


# Получаем путь к корневой директории проекта
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Главная страница админки.
@app.get("/admin/")
async def admin_page(request: Request):
    # Указываем путь к директории с шаблонами
    templates_dir = os.path.join("frontend", "admin")
    templates = Jinja2Templates(directory=templates_dir)
    return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/admin")
# def admin_stores(request: Request):
#     return HTMLResponse("frontend/admin/index.html", status_code=200)


# Список товаров, кнопки удаления, создания.
@app.get("/admin/products/")
async def admin_products(request: Request, db: AsyncSession = Depends(get_db)):
    templates_dir = os.path.join("frontend", "admin", "products")
    templates = Jinja2Templates(directory=templates_dir)
    products = await get_list_product(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})


# Удаление товаров.
@app.post("/admin/delete_products/")
async def delete_products(
    product_ids: List[int] = Form(...),  # Используем Form для получения данных из формы
    session: AsyncSession = Depends(get_db)  # Внедряем сессию базы данных
):
    await delete_selected(product_ids, session)  # Передаем сессию в функцию
    return RedirectResponse(url="/admin/products/", status_code=303)


# Внесение данных о новом товаре.
@app.get("/admin/product_form/", response_class=HTMLResponse)
async def product_form(request: Request, db: AsyncSession = Depends(get_db)):
    print("Внесение Данных о товаре")
    templates_dir = os.path.join("frontend", "admin", "products")
    templates = Jinja2Templates(directory=templates_dir)

    # Получаем список всех филиалов и категорий
    result = await db.execute(select(Store))
    stores = result.scalars().all()

    result = await db.execute(select(Category))
    categories = result.scalars().all()

    # Получаем данные о созданном товаре из сессии
    created_product = request.session.get("created_product", None)

    # Очищаем сессию после получения данных
    if "created_product" in request.session:
        del request.session["created_product"]

    # Передаем данные в шаблон
    return templates.TemplateResponse("create_product.html", {
        "request": request,
        "stores": stores,
        "categories": categories,
        "created_product": created_product if created_product else None
    })


# Создание нового товара.
@app.post("/admin/create_product/")
async def create_product_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    store_id: int = Form(...),
    category_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Создаем объект ProductCreate
    product_data = ProductCreate(
        name=name,
        description=description,
        price=price,
        store_id=store_id,
        category_id=category_id
    )

    # Создаем продукт в базе данных
    product = await create_product(db, product_data)

    # Получаем полные данные о филиале и категории
    store_result = await db.execute(select(Store).where(Store.id == store_id))
    store = store_result.scalars().first()

    category_result = await db.execute(select(Category).where(Category.id == category_id))
    category = category_result.scalars().first()

    # Проверяем, что store и category не равны None
    if store is None or category is None:
        raise HTTPException(status_code=404, detail="Store or Category not found")

    # Сохраняем информацию о созданном товаре в сессии
    request.session["created_product"] = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "store": {
            "id": store.id,
            "city": store.city,
            "address": store.address
        },
        "category": {
            "id": category.id,
            "name": category.name
        }
    }

    # Перенаправляем на страницу создания продукта
    return RedirectResponse(url="/admin/product_form/", status_code=303)


@app.get("/admin/categories")
def admin_categories(request: Request, db: Session = Depends(get_db)):
    # Указываем путь к директории с шаблонами
    templates_dir = os.path.join("frontend", "admin", "categories")
    templates = Jinja2Templates(directory=templates_dir)
    products = get_list_product(db)
    return templates.TemplateResponse("categories.html", {"request": request, "products": products})
