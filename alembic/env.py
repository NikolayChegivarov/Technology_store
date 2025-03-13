from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config import settings

# Добавляем наши модели для поддержки автогенерации миграций
from app.db.models import Store, Category, Product, User, CartItem, Order
from app.db.session import Base
target_metadata = Base.metadata

# это объект Alembic Config, который обеспечивает
# доступ к значениям в используемом файле .ini.
config = context.config

# Интерпретировать файл конфигурации для ведения журнала Python.
# Эта строка в основном настраивает регистраторы.
if config.config_file_name:
    fileConfig(config.config_file_name)


# Получаем URL базы данных из переменных окружения
DATABASE_URL = f"postgresql://{settings.USER_DB}:{settings.PASSWORD_DB}@{settings.HOST_DB}/{settings.NAME_DB}"

# Устанавливаем URL подключения к базе данных
config.set_main_option('sqlalchemy.url', DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()