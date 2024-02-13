from pydantic import EmailStr, Field, BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

from core.config import now_in_utc

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Address(BaseModel):
    street: str
    house: int
    house_add: str|None = None
    postcode: str
    city: str
    province: str|None = None
    country: str = "GERMANY"

    def __str__(self):
        return f"""
{self.street} {self.house} {self.house_add}
{self.postcode} {self.city}
{self.province}
{self.country}
        """


class UserBase(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    credit: int | None = Field(default=0, ge=0)
    address: Address | None = None
    is_active: bool = True


class UserUpdate(BaseModel):
    username: str | None = None
    fullname: str | None = None
    email: EmailStr | None = None
    address: Address | None = None


class UserIn(UserBase):
    plainpw: str


class UserDB(UserBase):
    id: int
    hashedpw: str
    created_at: datetime
    updated_at: datetime
    role: Role
    address: str | None = None
    picture_id: int

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    username: str
    created_at: datetime
    credit: int
    role: Role
    is_active: bool


class FullUserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    role: Role
    address: str | None = None


class UserBill(BaseModel):
    fullname: str
    address: str
    id: int
    email: EmailStr


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: int = Field(ge=0)
    stock: int = Field(default=0, ge=0)


class ItemIn(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class ItemDB(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemOut(ItemBase):
    def __str__(self):
        string = f"Name:\t{self.name}\nDesc:\t{self.description}\n"
        string += f"Price:\t{self.price/100.}\nStock:\t{self.stock}\n"
        return string


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class PasswordUpdate(BaseModel):
    new_pw: str


class AddCredit(BaseModel):
    amount: int = Field(gt=0)


class StockAmount(BaseModel):
    amount: int


class CartItem(BaseModel):
    item: ItemDB
    number: int = Field(gt=0)


class Post(BaseModel):
    item_id: int
    number: int = Field(gt=0)


class Cart(BaseModel):
    contents: list[CartItem] = []

    @property
    def total(self):
        s = 0
        for order in self.contents:
            s += order.item.price * order.number


class Order(BaseModel):
    contents: list[CartItem] = []
    customer: UserBill
    total: int
    date: datetime = now_in_utc()
    id: int
