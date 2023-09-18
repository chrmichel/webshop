from sqlalchemy.orm import Session

from util.schemes import UserIn
from util import User



MIKE = UserIn(fullname='Michael Biggs', username='mbiggie', email='mbiggs@cpd.gov', plainpw='mikepw', credit=5212)
MOLLY = UserIn(fullname='Molly Flynn', username='rollymolly', email='m.flynn@wpelem.gov', plainpw='mollypw')


def get_user(username: str, db: Session) -> User:
    user: User = db.query(User).filter(User.username == username).first()
    return user


def create_user(user: UserIn, db: Session) -> User:
    dbuser = User(
        fullname=user.fullname, username=user.username, email=user.email,
        hashedpw=user.plainpw, credit=user.credit
    )
    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)
    return dbuser


def delete_user(id: int, db: Session) -> None:
    db.query(User).filter(User.id == id).delete(False)


if __name__=="__main__":
    print(create_user(MIKE))