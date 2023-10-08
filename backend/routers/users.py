from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.schemas import UserIn, UserOut, FullUserOut, UserUpdate
from crud.users import (create_user, delete_user, get_user, get_all_users,
                        update_user)
from crud.errors import UsernameTakenError, EmailTakenError, NoSuchUserError
from db.models import User
from db.session import get_db
from .login import get_current_user


router = APIRouter()


@router.get('/all', response_model=list[UserOut])
def list_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get('/my-account', response_model=FullUserOut)
def my_account(user: User = Depends(get_current_user)):
    return user


@router.patch('/my-account', response_model=FullUserOut)
def update_account(
    new_data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_user(new_data, user, db)


@router.delete('/delete', status_code=204)
def delete_user_for_good(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_user(user.id, db)
    if not deleted:
        raise HTTPException(422, "User could not be deleted.")
    return


@router.get('/{username}', response_model=UserOut)
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    try:
        user = get_user(username, db)
    except NoSuchUserError as e:
        raise HTTPException(404, e.message)
    return user


@router.post('/register', response_model=UserOut, status_code=201)
def make_user(userdata: UserIn, db: Session = Depends(get_db)):
    try:
        user = create_user(userdata, db)
    except UsernameTakenError as u:
        raise HTTPException(451, u.message)
    except EmailTakenError as e:
        raise HTTPException(451, e.message)
    return user