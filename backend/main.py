from fastapi import FastAPI, Depends, Security, HTTPException
import uvicorn
import logging
from contextlib import asynccontextmanager

from util import host, port, engine, Base
from routers import user_router


logging.basicConfig(filename="main.log", level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("App started.")
    Base.metadata.create_all(bind=engine)
    yield
    logging.info("App finished.")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
async def start():
    return {"message": "Hello world"}


if __name__=="__main__":
    uvicorn.run(app='main:app', reload=True, host=host, port=port)
