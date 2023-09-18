from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from util.schemes import UserIn, UserOut
from util import User, get_db
from crud import users


router = APIRouter()


@router.get('/{username}', response_model=UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    user: User = users.get_user(username, db)
    if user is None:
        raise HTTPException(404)
    return user


@router.post('/new', response_model=UserOut)
def make_user(userdata: UserIn, db: Session = Depends(get_db)):
    user = users.create_user(userdata, db)
    return user