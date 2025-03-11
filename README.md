# Technology_store

This is a simple e-commerce API built with FastAPI.

## Running the project

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the server: `uvicorn app.main:app --reload`.

## Docker

To run the project in Docker:

```bash
docker build -t my_fastapi_project .
docker run -d -p 80:80 my_fastapi_project
```

Установите зависимости вручную:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose[cryptography] passlib python-multipart pydantic-settings pip install pytest email-validator
```
