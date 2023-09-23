from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from contextlib import asynccontextmanager

from util import host, port
from crud.users import startup
from routers import user_router, login_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(login_router, tags=["Login"])


@app.get("/")
async def start():
    return {"message": "Hello world"}


if __name__=="__main__":
    uvicorn.run(app='main:app', host=host, port=port)
