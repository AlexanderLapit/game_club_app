from sqlalchemy import Column, Integer, String, Float
from database.db import Base

class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    consumption_norm = Column(Float, nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    def __repr__(self):
        return f"<Material(id={self.id}, name='{self.name}', unit='{self.unit}', norm={self.consumption_norm}, cost={self.cost_per_unit})>"