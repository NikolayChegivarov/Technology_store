# Точка входа в приложение, где создается экземпляр FastAPI и подключаются роутеры.
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from app.api.v1.endpoints import products, cart, orders, users, auth, stores, category
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from app.db.session import get_db
from sqlalchemy.orm import Session
from frontend.admin.products.views_pr import get_list_product

app = FastAPI()

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


# Маршрут для главной страницы админки
@app.get("/admin")
async def admin_page(request: Request):
    print("=== Начало обработки запроса /admin ===")

    # Формируем путь к файлу относительно корневой директории
    frontend_path = os.path.join(BASE_PATH, "frontend", "admin", "index.html")
    print(f"Полный путь к файлу: {frontend_path}")

    try:
        # Проверяем существование файла
        print(f"Проверка существования файла: {os.path.exists(frontend_path)}")

        # Читаем содержимое файла
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("Файл успешно прочитан")
            return HTMLResponse(content, status_code=200)

    except FileNotFoundError:
        print(f"Ошибка: Файл {frontend_path} не найден")
        return HTMLResponse("Файл админ-панели не найден", status_code=500)

    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        return HTMLResponse("Внутренняя ошибка сервера", status_code=500)

# Указываем путь к директории с шаблонами
templates_dir = os.path.join("frontend", "admin", "products")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/admin/products/views_products", response_class=HTMLResponse)
async def views_products(request: Request, db: Session = Depends(get_db)):
    products = get_list_product(db)
    return templates.TemplateResponse("views_products.html", {"request": request, "products": products})


@app.get("/admin/stores")
def admin_stores(request: Request):
    return HTMLResponse("frontend/admin/index.html", status_code=200)


@app.get("/admin/categories")
def admin_categories(request: Request):
    return HTMLResponse("frontend/admin/index.html", status_code=200)
