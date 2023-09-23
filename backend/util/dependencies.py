from dotenv import dotenv_values
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


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