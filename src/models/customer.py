from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db import Base


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    inn = Column(String(12), unique=True)
    address = Column(String(200))
    phone = Column(String(20))
    is_buyer = Column(Boolean, default=False)
    is_salesman = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', inn='{self.inn}')>"