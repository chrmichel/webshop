from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from core.config import now_in_utc
from .base_class import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(60), unique=True)
    hashedpw: Mapped[str] = mapped_column(String(70))
    credit: Mapped[int]
    created_at: Mapped[datetime] = mapped_column("created at", DateTime, default=now_in_utc)
    updated_at: Mapped[datetime] = mapped_column("updated at", DateTime, default=now_in_utc, onupdate=now_in_utc)
    address: Mapped[str|None] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(10))
    is_active: Mapped[bool] = mapped_column(default=True)
    picture_id: Mapped[int] = mapped_column(ForeignKey("profile_pictures.id"), default=1)
    order_history: Mapped[list["Order"]] = relationship(back_populates="user")


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(70))
    description: Mapped[str] = mapped_column(String(200))
    price: Mapped[int]
    stock: Mapped[int]
    created_at: Mapped[datetime] = mapped_column("created at", DateTime, default=now_in_utc)
    updated_at: Mapped[datetime] = mapped_column("updated at", DateTime, default=now_in_utc, onupdate=now_in_utc)


class ProfilePicture(Base):
    __tablename__ = "profile_pictures"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_in_utc)
    path: Mapped[str] = mapped_column(String(64))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=now_in_utc)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    cart: Mapped["Cart"] = relationship("carts")
    user: Mapped["User"] = relationship(back_populates="order_history")


class Cart(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    posts: Mapped[list["Post"]] = relationship(back_populates="cart")


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    amount: Mapped[int]
    date_added: Mapped[datetime] = mapped_column(DateTime, default=now_in_utc)
    cart: Mapped["Cart"] = relationship(back_populates="posts")

