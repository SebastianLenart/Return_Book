from contextlib import contextmanager
from pprint import pprint

from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from configparser import ConfigParser
from psycopg2.pool import SimpleConnectionPool

CREATE_BOOKS = """CREATE TABLE IF NOT EXISTS books
(book_id SERIAL PRIMARY KEY, title TEXT, author TEXT, date_release INTEGER, is_borrow TEXT);"""
CREATE_BORROWER = """CREATE TABLE IF NOT EXISTS borrower
(borrower_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, debt INTEGER, book_id INTEGER, 
FOREIGN KEY(book_id) REFERENCES books (book_id));"""


class Database:
    def __init__(self):
        params = self.config()
        self.pool = SimpleConnectionPool(minconn=1, maxconn=10, **params)
        self.connection = None

    def __enter__(self):
        print("enter")
        self.connection = self.pool.getconn()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")
        if isinstance(exc_type, Exception):
            self.connection.rollback()
        self.pool.putconn(self.connection)

    @contextmanager
    def get_cursor(self):
        with self.connection:  # z tym dziala
            with self.connection.cursor() as cursor:
                yield cursor

    def config(self, filename='.env', section='postgresql'): # zbedne database.ini
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        print("****************")
        pprint(db)
        return db

    # ------------------------------------------------------------------------------------
    def create_tables(self):
        with self.get_cursor() as cursor:
            cursor.execute(CREATE_BOOKS)
            cursor.execute(CREATE_BORROWER)


