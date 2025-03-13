#  Здесь настраивается движок (engine), создается фабрика сессий (SessionLocal):
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# Создание движка с использованием URL строки
engine = create_engine(
    f"postgresql://{settings.USER_DB}:{settings.PASSWORD_DB}@{settings.HOST_DB}:{settings.PORT_DB}/{settings.NAME_DB}",
    echo=True
)

Base = declarative_base()

# Метод проверяет существующие таблицы и создает только те, которых нет
Base.metadata.create_all(bind=engine)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Функция для управления сессией базы данных с использованием контекстного менеджера.

    Yields:
        Session: Активная сессия базы данных

    Notes:
        - Создает новую сессию базы данных
        - Автоматически закрывает сессию после завершения работы
        - Используется как зависимость в FastAPI endpoints
        - Обеспечивает правильное управление ресурсами базы данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
