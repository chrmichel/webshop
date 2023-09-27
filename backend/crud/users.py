from sqlalchemy.orm import Session

from core.schemas import UserIn
from db.models import User
from .errors import NoSuchEmailError, NoSuchUserError, UsernameTakenError, EmailTakenError
from .hashing import Hasher


def get_user(username: str, db: Session) -> User:
    user: User = db.query(User).filter(User.username == username).first()
    if not user:
        raise NoSuchUserError(username)
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


def delete_user(id: int, db: Session) -> bool:
    deleted: bool = db.query(User).filter(User.id == id).delete(False)
    db.commit()
    return deleted
