from dotenv import load_dotenv
import os
from pathlib import Path

from core.schemas import UserIn

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

ADDRESS = "3529 Lincoln St, Chicago, IL"
MIKE = UserIn(
    fullname="Michael Biggs",
    username="mbiggie",
    email="mbiggs@cpd.gov",
    plainpw="mikepw",
    credit=5212,
)
MOLLY = UserIn(
    fullname="Molly Flynn",
    username="rollymolly",
    email="m.flynn@wpelem.gov",
    plainpw="mollypw",
)
ADMIN = UserIn(
    username="ADMIN", fullname="Ad Min", email="admin@web.shop", plainpw="adminpw"
)
