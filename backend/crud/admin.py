from sqlalchemy.orm import Session

from core.schemas import UserIn, Role
from crud.security import Hasher
from db.models import User

def new_admin(input: UserIn, db: Session) -> User:
    data_dict = input.model_dump()
    plainpw = data_dict.pop("plainpw")
    data_dict["hashedpw"] = Hasher.get_password_hash(plainpw)
    admin = User(**data_dict, role=Role.ADMIN.value)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin