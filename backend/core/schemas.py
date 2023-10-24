from pydantic import EmailStr, Field, BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    credit: int | None = Field(default=0, ge=0)
    address: str | None = None
    is_active: bool = True
    

class UserUpdate(BaseModel):
    username: str | None = None
    fullname: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class UserIn(UserBase):
    plainpw: str


class UserDB(UserBase):
    id: int
    hashedpw: str
    created_at: datetime
    updated_at: datetime
    role: Role

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


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: int = Field(ge=0)
    stock: int = Field(default=0, ge=0)


class ItemIn(ItemBase):
    pass


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
