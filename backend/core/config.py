from dotenv import load_dotenv
import os
from pathlib import Path
import datetime
from zoneinfo import ZoneInfo


def now_in_utc():
    return datetime.datetime.now(tz=ZoneInfo("UTC"))


env_path = Path(".") / ".env"
load_dotenv(env_path)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    APP_URL: str = os.getenv("APP_URL", "localhost")
    PORT: int = int(os.getenv("PORT", 8000))
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    TOKEN_EXPIRE_MINUTES: int = int(os.getenv("TOKEN_EXPIRE_MINUTES"))


settings = Settings()

ADDRESS = {
    "street": "5th Street",
    "house": 3674,
    "postcode": "8956V5",
    "city": "Chicago",
    "province": "Illinois",
    "country": "UNITED STATES",
}
MIKE = {
    "fullname": "Michael Biggs",
    "username": "mbiggie",
    "email": "mbiggs@cpd.gov",
    "plainpw": "mikepw",
    "credit": 5212,
}
MOLLY = {
    "fullname": "Molly Flynn",
    "username": "rollymolly",
    "email": "m.flynn@wpelem.gov",
    "plainpw": "mollypw",
}
ADMIN = {
    "username": "ADMIN",
    "fullname": "Ad Min",
    "email": "admin@web.shop",
    "plainpw": "adminpw",
}
PS5 = {
    "name": "PlayStation 5",
    "description": "Sony PS5 Gaming Console, 2 controllers included",
    "price": 44999,
    "stock": 300,
}
LAPTOP = {
    "name": "Dell XPS 15",
    "description": "Dell Gaming Laptop",
    "price": 149990,
    "stock": 40,
}
PROFILEPIC = "backend/static/images/emptyprofile.png"
