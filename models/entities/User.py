from flask_login import UserMixin


class User(UserMixin):
    
    def __init__(self, id, identity, password, phone="", name="", email="") -> None:
        self.id = id
        self.identity = identity
        self.password = password
        self.name = name
        self.phone = phone
        self.email = email
