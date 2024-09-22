from sqlite3 import connect


class Database:
    def __init__(self):
        self._connection = connect("./database.db")
        self._cursor = self._connection.cursor()

    def init(self): 
        self._cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if self._cursor.fetchone() is None:
            with open("schema.sql", "r") as f:
                schema = f.read()
            self._cursor.executescript(schema)
            self._connection.commit()

        self._connection.close()   
        
    def __del__(self):
        self._connection.close()
