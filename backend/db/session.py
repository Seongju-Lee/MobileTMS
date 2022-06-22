from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# For postgrSQL database
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=500)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
