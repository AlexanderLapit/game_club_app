from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    unit = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', unit='{self.unit}', price={self.price})>"