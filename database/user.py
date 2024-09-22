from sqlite3 import connect


class UserQueries:
    def __init__(self):
        self._connection = connect("./database.db")
        self._cursor = self._connection.cursor()

    def get_all(self):
        data = self._cursor.execute("SELECT * FROM users")
        return data.fetchall()

    def get_user(self, username):
        user = self._cursor.execute(
            f"SELECT * FROM users WHERE username = '{username}'"
        )
        return user.fetchone()

    def create_user_db(self, user):
        self._cursor.execute(
            f"""INSERT INTO users (username, first_name, last_name, password)
                VALUES('{user['username']}', '{user['first_name']}', '{user['last_name']}', '{user['password']}')
            """
        )
        self._connection.commit()

    def __del__(self):
        self._connection.close()
