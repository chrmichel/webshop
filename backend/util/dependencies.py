from dotenv import dotenv_values
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .database import Base
from crud.users import get_user, create_user, MIKE, MOLLY


cfg = dotenv_values(os.path.join(os.path.dirname(__file__), "../../.env"))
port = int(cfg.get("PORT"))
host = cfg.get("APP_URL")
db_url = cfg.get("DATABASE_URL")


engine = create_engine(db_url, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        mike_in_db = get_user(MIKE.username, db)
        if not mike_in_db:
            create_user(MIKE, db)
        molly_in_db = get_user(MOLLY.username, db)
        if not molly_in_db:
            create_user(MOLLY, db)
