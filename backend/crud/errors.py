class EmailTakenError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        self.message = "This email is already associaed with an account. Please use the associated account or use another email."
        super().__init__(self.message)


class UsernameTakenError(Exception):
    def __init__(self, username: str) -> None:
        self.username = username
        self.message = "This username is already taken. Please use another."
        super().__init__(self.message)


class NoSuchUserError(Exception):
    def __init__(self, username: str) -> None:
        self.username = username
        self.message = "No username found with this name."
        super().__init__(self.message)


class NoSuchEmailError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        self.message = "This email is not associated with any account."
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "You are not authorized for this action."
        super().__init__(self.message, *args)


class WrongPasswordError(Exception):
    pass