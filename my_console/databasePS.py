from contextlib import contextmanager
from pprint import pprint

from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from configparser import ConfigParser
from psycopg2.pool import SimpleConnectionPool

CREATE_BOOKS = """CREATE TABLE IF NOT EXISTS books
(book_id SERIAL PRIMARY KEY, title TEXT, author TEXT, date_release TEXT, is_borrow TEXT);"""
CREATE_BORROWER = """CREATE TABLE IF NOT EXISTS borrower
(borrower_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, debt INTEGER, book_id INTEGER, 
FOREIGN KEY(book_id) REFERENCES books (book_id));"""

INSERT_BOOK_RETURN_ID = """INSERT INTO books (title, author, date_release, is_borrow) VALUES (%s, %s, %s, %s) 
RETURNING book_id;"""
INSERT_BORROWER_RETURN_ID = """INSERT INTO borrower (first_name, last_name, email,
debt, book_id) VALUES (%s, %s, %s, %s, %s) RETURNING borrower_id;"""

SELECT_ALL_BOOKS = """SELECT * FROM books;"""
SELECT_BOOKS_BY_TITLE = """SELECT * FROM books WHERE title = %s;"""
SELECT_ALL_BORROWERS = """SELECT * FROM borrower ORDER BY borrower_id;"""
SELECT_BORROWERS_BY_NAME = """SELECT * FROM borrower WHERE first_name = %s AND last_name = %s;"""

DELETE_BOOK_BY_TITLE = """DELETE FROM books WHERE title=%s RETURNING*;"""
DELETE_BOOK_BY_ID = """DELETE FROM books WHERE book_id=%s RETURNING*;"""
DELETE_BORROWER_BY_NAME = """DELETE FROM borrower WHERE first_name = %s AND last_name = %s
RETURNING*;"""
DELETE_BORROWER_BY_ID = """DELETE FROM borrower WHERE borrower_id = %s RETURNING*; """

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

    def config(self, filename='.env', section='postgresql'):  # zbedne database.ini
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

    def add_book(self, title, author, date_release, is_borrow):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_BOOK_RETURN_ID, (title, author, date_release, is_borrow))
            return cursor.fetchone()[0]

    def get_books(self):  # -> List["Books"]: dopkoncz to !!!
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_ALL_BOOKS)
            return cursor.fetchall()

    def get_books_by_title(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BOOKS_BY_TITLE, (title,))
            return cursor.fetchall()

    def remove_book_by_title(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_BOOK_BY_TITLE, (title,))
            return cursor.fetchall()[0]

    def remove_book_by_id(self, id):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_BOOK_BY_ID, (id,))
            return cursor.fetchall()[0]

    def add_borrower(self, first_name, last_name, email, debt, book_id):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_BORROWER_RETURN_ID, (first_name, last_name, email, debt, book_id))
            return cursor.fetchone()[0]

    def get_all_borrowers(self):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_ALL_BORROWERS)
            return cursor.fetchall()

    def get_borrowers_by_name(self, fname, lname):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BORROWERS_BY_NAME, (fname, lname))
            return cursor.fetchall()

    def remove_borrowers_by_name(self, fname, lname):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_BORROWER_BY_NAME, (fname, lname))
            return cursor.fetchall()[0]