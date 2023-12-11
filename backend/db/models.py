from sqlalchemy import Column, Integer, String, Boolean, DateTime

from core.config import now_in_utc
from .base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(30), unique=True, nullable=False)
    fullname = Column("fullname", String(50), index=True, nullable=False)
    email = Column("email", String(50), unique=True, nullable=False)
    hashedpw = Column("hashedpw", String(70))
    credit = Column("credit", Integer)
    created_at = Column("created at", DateTime, default=now_in_utc)
    updated_at = Column("updated at", DateTime, default=now_in_utc, onupdate=now_in_utc)
    address = Column("address", String(200))
    role = Column("role", String(10))
    is_active = Column("is active", Boolean, default=True)


class Item(Base):
    __tablename__ = "items"
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(70), index=True)
    description = Column("description", String(200))
    price = Column("price", Integer)
    stock = Column("stock", Integer)
    created_at = Column("created at", DateTime, default=now_in_utc)
    updated_at = Column("updated at", DateTime, default=now_in_utc, onupdate=now_in_utc)
