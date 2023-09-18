from fastapi import FastAPI, Depends, Security, HTTPException
import uvicorn
import logging
from contextlib import asynccontextmanager

from util import host, port, startup
from routers import user_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started.")
    startup()
    yield
    logger.info("App finished.")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
async def start():
    return {"message": "Hello world"}


if __name__=="__main__":
    uvicorn.run(app='main:app', reload=True, host=host, port=port)
