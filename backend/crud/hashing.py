from passlib.context import CryptContext


class Hasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)