from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import datetime

from .base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(30), unique=True, nullable=False)
    fullname = Column("fullname", String(50), index=True, nullable=False)
    email = Column("email", String(50), unique=True, nullable=False)
    hashedpw = Column("hashedpw", String(70))
    credit = Column("credit", Integer)
    created_at = Column("created at", DateTime, default=datetime.datetime.now)
    updated_at = Column("updated at", DateTime, default=datetime.datetime.now)
    address = Column("address", String(200))
    role = Column("role", String(10))


class Item(Base):
    __tablename__ = "items"
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(70), index=True)
    description = Column("description", String(200))
    price = Column("price", Integer)
    stock = Column("stock", Integer)
    created_at = Column("created at", DateTime, default=datetime.datetime.utcnow)
    updated_at = Column("updated at", DateTime, default=datetime.datetime.utcnow)