from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import dotenv_values
import os

from util.schemes import UserIn
from util import User, Base, engine, SessionLocal
from .errors import NoSuchEmailError, NoSuchUserError, UsernameTakenError, EmailTakenError


MIKE = UserIn(fullname='Michael Biggs', username='mbiggie', email='mbiggs@cpd.gov', plainpw='mikepw', credit=5212)
MOLLY = UserIn(fullname='Molly Flynn', username='rollymolly', email='m.flynn@wpelem.gov', plainpw='mollypw')

cfg = dotenv_values(os.path.join(os.path.dirname(__file__), "../../.env"))
key = cfg.get("KEY")
alg = cfg.get("ALGORITHM")
token_exp_min = int(cfg.get("TOKEN_EXPIRE_MINUTES"))

def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        try:
            mike_in_db = get_user(MIKE.username, db)
        except NoSuchUserError:
            create_user(MIKE, db)
        try:
            molly_in_db = get_user(MOLLY.username, db)
        except NoSuchUserError:
            create_user(MOLLY, db)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)



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
        hashedpw=get_password_hash(user.plainpw), credit=user.credit
    )
    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)
    return dbuser


def authenticate_user(username: str, pw: str, db: Session) -> bool | User:
    try:
        user = get_user(username, db)
    except NoSuchUserError:
        return False
    if not verify_password(pw, user.hashedpw):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=token_exp_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=alg)
    return encoded_jwt


def delete_user(name: str, db: Session) -> bool:
    deleted: bool = db.query(User).filter(User.username == name).delete(False)
    db.commit()
    return deleted
