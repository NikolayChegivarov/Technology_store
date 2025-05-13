# Technology_store

Магазин электроники, техники, инструмента, созданный с помощью FastAPI.

1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение.
3. Установите зависимости командой:
```bash
pip install -r requirements.txt 
```
или установить их вручную:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose[cryptography] passlib python-multipart pydantic-settings pytest email-validator sqlalchemy[asyncio] asyncpg
pip install itsdangerous python-multipart 
pip install alembic
pip install jinja2
```
4. Создать базу данных.
5. Выполните миграции:
```bash
alembic upgrade head
```
6. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

## Docker

To run the project in Docker:

```bash
docker build -t my_fastapi_project .
docker run -d -p 80:80 my_fastapi_project
```

