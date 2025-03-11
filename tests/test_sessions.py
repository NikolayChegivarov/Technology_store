import pytest
from app.db.session import SessionLocal, engine, Base
from sqlalchemy import Column, Integer
from sqlalchemy import String


@pytest.fixture(scope="session")
def test_db():
    """Фикстура для создания тестовой базы данных"""
    # Создаем все таблицы в тестовой базе
    Base.metadata.create_all(bind=engine)

    yield engine

    # Удаляем все таблицы после завершения всех тестов
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Фикстура для создания новой сессии базы данных"""
    connection = test_db.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    # Откатываем все изменения после каждого теста
    session.close()
    transaction.rollback()
    connection.close()


def test_get_db():
    """Тестируем функцию get_db()"""
    db = SessionLocal()
    assert db.bind == engine
    db.close()


def test_database_connection(db_session):
    """Тестируем подключение к базе данных"""
    assert db_session.bind == engine
    assert db_session.query(Base).count() == 0


def test_transaction_rollback(db_session):
    """Тестируем работу транзакций"""

    # Создаем тестовый объект
    class TestModel(Base):
        __tablename__ = "test_model"
        id = Column(Integer, primary_key=True)
        name = Column(String)

    # Добавляем объект
    obj = TestModel(name="test")
    db_session.add(obj)
    db_session.commit()

    # Проверяем, что объект добавлен
    assert db_session.query(TestModel).count() == 1

    # Откатываем изменения
    db_session.rollback()

    # Проверяем, что объект удален
    assert db_session.query(TestModel).count() == 0
