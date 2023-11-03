from sqlalchemy.orm import Session
from datetime import datetime, timezone

from core.schemas import ItemIn, ItemUpdate
from db.models import Item
from .errors import NoSuchItemError, ItemNameTakenError


def get_item(id: int, db: Session) -> Item:
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise NoSuchItemError(id)
    return item


def get_item_name(name: str, db: Session) -> Item:
    item = db.query(Item).filter(Item.name == name).first()
    if not item:
        raise NoSuchItemError(id)
    return item


def get_all_items(db: Session) -> list[Item]:
    items = db.query(Item).all()
    return items


def search_items(text: str, db: Session) -> list[Item]:
    items = (
        db.query(Item).filter((text in Item.name) or (text in Item.description)).all()
    )
    return items


def create_item(item_in: ItemIn, db: Session) -> Item:
    data = item_in.model_dump()
    name = data["name"]
    check = db.query(Item).filter(Item.name == name).first()
    if check:
        raise ItemNameTakenError(name)
    item = Item(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(id: int, item_up: ItemUpdate, db: Session) -> Item:
    data = item_up.model_dump(exclude_defaults=True)
    data["updated_at"] = datetime.now()
    upd = db.query(Item).filter(Item.id == id).update(data)
    if not upd:
        raise NoSuchItemError(id)
    db.commit()
    return get_item(id, db)


def delete_item(id: int, db: Session) -> bool:
    dlt = db.query(Item).filter(Item.id == id).delete(False)
    if not dlt:
        raise NoSuchItemError(id)
    db.commit()
    return dlt


def change_stock_amount(id: int, amount: int, db: Session) -> int:
    item = get_item(id, db)
    new = item.stock + amount
    if new < 0:
        raise ValueError
    upd = db.query(Item).filter(Item.id == id).update({"stock": new})
    if not upd:
        raise Exception
    db.commit()
    return new
