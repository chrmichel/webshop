from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from core.config import MIKE, MOLLY, settings
from crud.errors import NoSuchUserError
from crud.users import get_user, create_user
from db.base_class import Base
from db.session import engine, SessionLocal
from routers.users import router as user_router
from routers.login import router as login_router


def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        try:
            _ = get_user(MIKE.username, db)
        except NoSuchUserError:
            create_user(MIKE, db)
        try:
            _ = get_user(MOLLY.username, db)
        except NoSuchUserError:
            create_user(MOLLY, db)



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
    uvicorn.run(app='main:app', host=settings.APP_URL, port=settings.PORT)
