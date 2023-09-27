from sqlalchemy import Column, Integer, String, ForeignKey

from .base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(30), unique=True, nullable=False)
    fullname = Column("fullname", String(50), index=True, nullable=False)
    email = Column("email", String(50), unique=True, nullable=False)
    hashedpw = Column("hashedpw", String(70))
    credit = Column("credit", Integer)


class Item(Base):
    __tablename__ = "items"
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(30), index=True)
    description = Column("description", String(200))
    price = Column("price", Integer)
    stock = Column("stock", Integer)
    vendor_id = Column("vendor_id", ForeignKey("users.id"))