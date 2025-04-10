from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Создание асинхронного движка
engine = create_async_engine(
    f"postgresql+asyncpg://{settings.USER_DB}:{settings.PASSWORD_DB}@"
    f"{settings.HOST_DB}:{settings.PORT_DB}/{settings.NAME_DB}",
    echo=True
)

Base = declarative_base()

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    """
    Асинхронная функция для управления сессией базы данных.

    Yields:
        AsyncSession: Активная асинхронная сессия базы данных
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
