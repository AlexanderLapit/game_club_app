from sqlalchemy import Column, Integer, String, Numeric
from database.db import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    unit = Column(String(50), nullable=False, default="шт")
    price = Column(Numeric(precision=10, scale=2), nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"