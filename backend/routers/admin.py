from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from core.schemas import UserIn, UserOut
from crud.admin import new_admin
from db.session import get_db
from .login import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def create_admin(admin_data: UserIn, db: Session = Depends(get_db)):
    return new_admin(admin_data, db)


@router.put("/ban/{user_id}",
            dependencies=[Security(get_current_active_user, scopes=["admin"])])
def ban_user(user_id: int, db: Session = Depends(get_db)):
    pass