from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.schemas import (
    UserIn,
    UserOut,
    FullUserOut,
)
from crud.users import (
    create_user,
    get_user,
    get_all_users,
)
from crud.errors import UsernameTakenError, EmailTakenError, NoSuchUserError
from db.session import get_db


router = APIRouter()


@router.get("/all", response_model=list[UserOut])
def list_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.post("/register", response_model=UserOut, status_code=201)
def make_user(userdata: UserIn, db: Session = Depends(get_db)):
    try:
        user = create_user(userdata, db)
    except UsernameTakenError as u:
        raise HTTPException(451, u.message)
    except EmailTakenError as e:
        raise HTTPException(451, e.message)
    return user


@router.get("/{username}", response_model=FullUserOut)
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    try:
        user = get_user(username, db)
    except NoSuchUserError as e:
        raise HTTPException(404, e.message)
    return user
