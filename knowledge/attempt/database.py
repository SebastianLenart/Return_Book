import sqlite3


# Version 2
class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
