from fastapi import APIRouter, Depends, HTTPException, Security, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import uuid

from core.schemas import (
    UserOut,
    FullUserOut,
    UserUpdate,
    PasswordUpdate,
    AddCredit,
    UserDB,
)
from crud.users import (
    delete_user,
    update_user,
    reset_password,
    more_money,
)
from crud.pictures import get_picture_path, add_pic_to_db
from db.models import User
from db.session import get_db
from .login import get_current_active_user

myacc = APIRouter()


@myacc.get("/", response_model=UserDB)
def my_account(user: User = Security(get_current_active_user)):
    return user


@myacc.patch("/", response_model=FullUserOut)
def update_account(
    new_data: UserUpdate,
    user: User = Security(get_current_active_user),
    db: Session = Depends(get_db),
):
    return update_user(new_data, user, db)


@myacc.delete("/", status_code=204)
def delete_user_for_good(
    user: User = Security(get_current_active_user), db: Session = Depends(get_db)
):
    deleted = delete_user(user.id, db)
    if not deleted:
        raise HTTPException(422, "User could not be deleted.")
    return


@myacc.post("/reset-password", response_model=UserOut)
def password_reset(
    new_pw: PasswordUpdate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return reset_password(new_pw.new_pw, user, db)


@myacc.post("/add-credit", response_model=UserOut)
def add_credit(
    credit_addition: AddCredit,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return more_money(credit_addition.amount, user, db)


@myacc.get("/picture", response_class=FileResponse)
def get_picture(
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    print(pid := user.picture_id)
    path = get_picture_path(pid, db)
    ending = path.split(".")[-1]
    return FileResponse(path, media_type=f"image/{ending}")

@myacc.post("/upload-picture")
def upload_profile_pic(
    file: UploadFile = File(...),
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    pic_type = file.filename.split(".")[-1]
    path = f"backend/static/images/{uuid.uuid4()}.{pic_type}"
    try:
        with open(path, "w+b") as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error during uploading."}
    pic = add_pic_to_db(path, db)
    user.picture_id = pic.id
    db.commit()
    db.refresh(user)
    return {"message": "Profile picture successfully updated."}