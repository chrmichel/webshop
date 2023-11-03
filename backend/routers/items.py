from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from core.schemas import ItemIn, ItemOut, ItemUpdate, StockAmount
from crud.errors import NoSuchItemError, ItemNameTakenError
from crud.items import (
    get_item,
    get_all_items,
    create_item,
    update_item,
    delete_item,
    change_stock_amount,
)
from db.session import get_db

from .login import get_admin


router = APIRouter()
admin = APIRouter(dependencies=[Security(get_admin)], tags=["Admin"])


@router.get("/all", response_model=list[ItemOut])
def show_all_items(db: Session = Depends(get_db)):
    return get_all_items(db)


@router.get("/{id}", response_model=ItemOut)
def retrieve_item(id: int, db: Session = Depends(get_db)):
    try:
        item = get_item(id, db)
    except NoSuchItemError as e:
        raise HTTPException(404, e.message)
    return item


@admin.patch("/{id}", response_model=ItemOut)
def change_item(id: int, update: ItemUpdate, db: Session = Depends(get_db)):
    try:
        item = update_item(id, update, db)
    except NoSuchItemError as e:
        raise HTTPException(404, e.message)
    return item


@admin.delete("/{id}", status_code=204)
def remove_item(id: int, db: Session = Depends(get_db)):
    try:
        _ = delete_item(id, db)
    except NoSuchItemError as e:
        raise HTTPException(404, e.message)


@admin.post("/new", response_model=ItemOut, status_code=201)
def new_item(item: ItemIn, db: Session = Depends(get_db)):
    try:
        dbitem = create_item(item, db)
    except ItemNameTakenError as e:
        raise HTTPException(404, e.message)
    return dbitem


@admin.post("/{id}/restock", response_model=StockAmount)
def change_inventory(id: int, change: StockAmount, db: Session = Depends(get_db)):
    try:
        new_num = change_stock_amount(id, change.amount, db)
    except:
        raise HTTPException(404)
    return StockAmount(amount=new_num)


router.include_router(admin)
