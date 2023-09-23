from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from util.schemes import UserIn, UserOut
from util import get_db, User
from crud import users, errors
from .login import get_current_user


router = APIRouter()


@router.get('/{username}', response_model=UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    try:
        user = users.get_user(username, db)
    except errors.NoSuchUserError as e:
        raise HTTPException(404, e.message)
    return user


@router.post('/new', response_model=UserOut, status_code=201)
def make_user(userdata: UserIn, db: Session = Depends(get_db)):
    try:
        user = users.create_user(userdata, db)
    except errors.UsernameTakenError as u:
        raise HTTPException(422, u.message)
    except errors.EmailTakenError as e:
        raise HTTPException(422, e.message)
    return user


@router.delete('/me', status_code=204)
def delete_user(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = users.delete_user(user.username, db)
    if not deleted:
        raise HTTPException(422, "User could not be deleted.")
    return