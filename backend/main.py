from fastapi import FastAPI
import uvicorn
import logging
from dotenv import dotenv_values
import os
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


logging.basicConfig(filename="main.log", level=logging.INFO)


cfg = dotenv_values(os.path.join(os.path.dirname(__file__), "../.env"))
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("App started.")
    yield
    logging.info("App finished.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def start():
    return {"message": "Hello world"}


if __name__=="__main__":
    uvicorn.run(app='main:app', reload=True, host=host, port=port)
