from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Construct database URL
DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://postgres:password@localhost:5432/lwk_scraping')
# If using Railway, they provide a PostgreSQL URL that needs to be modified for SQLAlchemy
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'torque_rods'

    id = Column(Integer, primary_key=True)
    sku = Column(String)
    type1 = Column(String)
    type2 = Column(String)
    c_to_c = Column(String)
    side_a = Column(String)
    side_b = Column(String)
    side_a_bushing = Column(String)
    side_b_bushing = Column(String)
    side_a_angle = Column(String)
    side_b_angle = Column(String)
    shaft_dia = Column(String)
    notes = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
