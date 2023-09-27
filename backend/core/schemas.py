from pydantic import EmailStr, Field, BaseModel


class UserBase(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    credit: int = Field(default=0, ge=0)


class UserIn(UserBase):
    plainpw: str


class UserDB(UserBase):
    id: int
    hashedpw: str

    class Config:
        orm_mode = True


class UserOut(UserBase):
    def __str__(self):
        string = f"Name:\t{self.fullname}\nEmail:\t{self.email}\n"
        string += f"Credit:\t{self.credit/100.}\n"
        return string


class ItemBase(BaseModel):
    name: str
    description: str | None
    price: int = Field(default=0, ge=0)
    stock: int = Field(default=0, ge=0)


class ItemIn(ItemBase):
    pass


class ItemDB(ItemBase):
    id: int
    vendor_id: int

    class Config:
        orm_mode = True


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

    
if __name__ == '__main__':
    apple = ItemOut(name='apple', description="delicious", price=299, stock=6)
    print(apple)
    mike = UserOut(fullname='Michael Biggs', email='mbiggs@cpd.gov', credit=5212)
    print(mike)