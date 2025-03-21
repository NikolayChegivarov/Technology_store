from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, index=True)

    products = relationship("Product", back_populates="store")

    def __repr__(self):
        return f"Store(name='{self.name}', city='{self.city}')"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Связь с продуктами
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"Category(name='{self.name}')"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    store_id = Column(Integer, ForeignKey("stores.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")

    def to_dict(self) -> dict:
        """Преобразует объект продукта в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "store_id": self.store_id,
            "category_id": self.category_id,
            "store": {
                "id": self.store.id,
                "city": self.store.city,
                "address": self.store.address
            } if self.store else None,
            "category": {
                "id": self.category.id,
                "name": self.category.name
            } if self.category else None
        }


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship("Order", back_populates="user")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)

    user = relationship("User", back_populates="orders")