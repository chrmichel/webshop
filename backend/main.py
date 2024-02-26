from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager

from core.config import ADMIN, MIKE, MOLLY, PS5, LAPTOP, PROFILEPIC, settings
from core.schemas import UserIn, ItemIn
from crud.admin import new_admin
from crud.errors import NoSuchItemError, NoSuchUserError
from crud.items import get_item_name, create_item
from crud.pictures import get_picture_path, add_pic_to_db
from crud.users import get_user, create_user
from db.base_class import Base
from db.session import engine, SessionLocal
from routers.admin import router as admin_router
from routers.items import router as item_router
from routers.login import router as login_router
from routers.my_account import myacc
from routers.users import router as user_router


def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        try:
            _ = get_user(ADMIN["username"], db)
        except NoSuchUserError:
            _ = new_admin(UserIn(**ADMIN), db)
        try:
            _ = get_user(MIKE["username"], db)
        except NoSuchUserError:
            _ = create_user(UserIn(**MIKE), db)
        try:
            _ = get_user(MOLLY["username"], db)
        except NoSuchUserError:
            _ = create_user(UserIn(**MOLLY), db)
        try:
            _ = get_item_name(PS5["name"], db)
        except NoSuchItemError:
            _ = create_item(ItemIn(**PS5), db)
        try:
            _ = get_item_name(LAPTOP["name"], db)
        except NoSuchItemError:
            _ = create_item(ItemIn(**LAPTOP), db)
        try:
            _ = get_picture_path(1, db)
        except Exception:
            add_pic_to_db(PROFILEPIC, db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup()
    app.include_router(admin_router, prefix="/admin", tags=["Admin"])
    app.include_router(user_router, prefix="/users", tags=["Users"])
    app.include_router(login_router, tags=["Login"])
    app.include_router(item_router, prefix="/items", tags=["Items"])
    app.include_router(myacc, prefix="/my-account", tags=["My account"])
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def start():
    return RedirectResponse("/docs")


@app.get("/wish", include_in_schema=False)
def get_icon():
    return FileResponse("backend/static/images/wishicon.png")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=settings.APP_URL, port=settings.PORT, reload=True)
