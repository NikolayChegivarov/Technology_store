# Точка входа в приложение, где создается экземпляр FastAPI и подключаются роутеры.
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints import products, cart, orders, users, auth, stores, category
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

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


# # Редирект с корневого пути на index.html
# @app.get("/")
# async def read_root():
#     return RedirectResponse(url="/static/index.html")  # Перенаправляем на index.html
#
#
# @app.get("/admin")
# async def admin_redirect():
#     return RedirectResponse(url="/static/admin/index.html")


# Маршрут для главной страницы админки
@app.get("/admin")
def admin_page(request: Request):
    return HTMLResponse("frontend/admin/index.html", status_code=200)


# Маршруты для вкладок админки
@app.get("/admin/products")
def admin_products(request: Request):
    return HTMLResponse("frontend/admin/index.html", status_code=200)


@app.get("/admin/stores")
def admin_stores(request: Request):
    return HTMLResponse("frontend/admin/index.html", status_code=200)


@app.get("/admin/categories")
def admin_categories(request: Request):
    return HTMLResponse("frontend/admin/index.html", status_code=200)
