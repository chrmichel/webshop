class EmailTakenError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        self.message = f"""The email {email} is already associaed with an account.
                        Please use the associated account or use another email."""
        super().__init__(self.message)


class UsernameTakenError(Exception):
    def __init__(self, username: str) -> None:
        self.username = username
        self.message = f"Username {username} is already taken. Please use another."
        super().__init__(self.message)


class NoSuchUserError(Exception):
    def __init__(self, username: str) -> None:
        self.username = username
        self.message = f"No user found with username {username}."
        super().__init__(self.message)


class NoSuchEmailError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        self.message = f"The email {email} is not associated with any account."
        super().__init__(self.message)


class InvalidAmountError(Exception):
    def __init__(self, amount: int | float) -> None:
        self.amount = amount
        self.message = f"""The chosen amount {amount} is invalid, please choose 
        an amount that is positive and in whole cents."""
        super().__init__(self.message)


class NoSuchItemError(Exception):
    def __init__(self, id: int) -> None:
        self.item_id = id
        self.message = f"No item with {id = } found."
        super().__init__(self.message)


class ItemNameTakenError(Exception):
    def __init__(self, name: str) -> None:
        self.item_name = name
        self.message = f"Item with {name = } exists already. Choose another name."
        super().__init__(self.message)
