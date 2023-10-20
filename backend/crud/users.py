from sqlalchemy.orm import Session

from core.schemas import UserIn, UserUpdate
from db.models import User
from .errors import NoSuchEmailError, NoSuchUserError, UsernameTakenError,\
    EmailTakenError
from .hashing import Hasher


def get_user(username: str, db: Session) -> User:
    user: User = db.query(User).filter(User.username == username).first()
    if not user:
        raise NoSuchUserError(username)
    return user


def get_user_id(id: int, db: Session) -> User:
    user: User = db.query(User).filter(User.id == id).first()
    if not user:
        raise NoSuchUserError(id)
    return user


def get_user_mail(email: str, db: Session) -> User:
    user: User = db.query(User).filter(User.email == email).first()
    if not user:
        raise NoSuchEmailError(email)
    return user


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(user: UserIn, db: Session) -> User:
    try:
        namecheck = get_user(user.username, db)
        raise UsernameTakenError(namecheck.username)
    except NoSuchUserError:
        pass

    try:
        mailcheck = get_user_mail(user.email, db)
        raise EmailTakenError(mailcheck.email)
    except NoSuchEmailError:
        pass

    dbuser = User(
        fullname=user.fullname, username=user.username, email=user.email,
        hashedpw=Hasher.get_password_hash(user.plainpw), credit=user.credit
    )
    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)
    return dbuser


def update_user(new_data: UserUpdate, user: User, db: Session) -> User:
    update_dict = new_data.model_dump(exclude_unset=True)
    db.query(User).filter(User.id == user.id).update(update_dict)
    db.commit()
    return get_user_id(user.id, db)


def reset_password(new_pw: str, user: User, db: Session) -> User:
    hashedpw = Hasher.get_password_hash(new_pw)
    db.query(User).filter(User.id == user.id).update({"hashedpw": hashedpw})
    db.commit()
    return get_user_id(user.id, db)


def delete_user(id: int, db: Session) -> bool:
    deleted: bool = db.query(User).filter(User.id == id).delete(False)
    db.commit()
    return deleted


def more_money(amount: int, user: User, db: Session) -> User:
    
    db.query(User).filter(User.id == user.id)\
        .update({"credit": user.credit + amount})
    db.commit()
    return get_user_id(user.id, db)