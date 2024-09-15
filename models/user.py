from database.user import UserQueries
from werkzeug.security import generate_password_hash


class User:
    def __init__(self, user_data):
        self.db = UserQueries()
        self.user_data = user_data

    def create_user(self):
        self.__password_encryption()
        self.db.create_user_db(self.user_data)

    def __password_encryption(self):
        self.user_data["password"] = generate_password_hash(
            self.user_data["password"], "pbkdf2:sha256:30", 30
        )
