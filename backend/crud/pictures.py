from sqlalchemy.orm import Session

from db.models import ProfilePicture


def add_pic_to_db(path: str, db: Session) -> ProfilePicture:
    pic_db = ProfilePicture(path=path)
    db.add(pic_db)
    db.commit()
    db.refresh(pic_db)
    return pic_db


def get_picture_path(id: int, db: Session) -> str:
    pic: ProfilePicture = (
        db.query(ProfilePicture).filter(ProfilePicture.id == id).first()
    )
    if pic:
        return pic.path
    raise ValueError(f"No picture with id {id}")
