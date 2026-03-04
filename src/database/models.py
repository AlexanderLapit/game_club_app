from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.db import Base
class AccessLevel(Base):
    __tablename__ = 'access_levels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    users = relationship('User', back_populates='access_level')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    access_level_id = Column(Integer, ForeignKey('access_levels.id'))
    is_active = Column(Boolean, default=True)
    access_level = relationship('AccessLevel', back_populates='users')

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    inn = Column(String(12))
    address = Column(String(200))
    phone = Column(String(20))
    is_buyer = Column(Boolean, default=False)
    is_salesman = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)

class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    consumption_norm = Column(Float)