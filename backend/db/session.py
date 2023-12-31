from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from core.config import settings


engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
