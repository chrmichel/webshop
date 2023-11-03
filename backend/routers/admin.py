from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from core.schemas import UserIn, UserOut
from crud.admin import new_admin, set_user_inactive, set_user_active
from db.session import get_db
from .login import get_current_active_user

router = APIRouter()


@router.get("/", dependencies=[Security(get_current_active_user, scopes=["admin"])])
def check_admin_access():
    return {"is admin"}


@router.post("/register", response_model=UserOut, status_code=201)
def create_admin(admin_data: UserIn, db: Session = Depends(get_db)):
    return new_admin(admin_data, db)


@router.put(
    "/ban/{username}",
    dependencies=[Security(get_current_active_user, scopes=["admin"])],
    response_model=UserOut,
)
def ban_user(username: str, db: Session = Depends(get_db)):
    return set_user_inactive(username, db)


@router.put(
    "/unban/{username}",
    dependencies=[Security(get_current_active_user, scopes=["admin"])],
    response_model=UserOut,
)
def unban_user(username: str, db: Session = Depends(get_db)):
    return set_user_active(username, db)
