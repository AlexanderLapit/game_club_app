from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from models.access_levels import AccessLevel
    from models.customer import Customer
    from models.product import Product
    from models.material import Material
    from models.user import User
    from models.order import Order  # Только после Customer!
    Base.metadata.create_all(bind=engine)