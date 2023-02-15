from contextlib import contextmanager
from pprint import pprint

from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from configparser import ConfigParser
from psycopg2.pool import SimpleConnectionPool

CREATE_BOOKS = """CREATE TABLE IF NOT EXISTS books
(book_id SERIAL PRIMARY KEY, title TEXT, author TEXT, date_release TEXT,
borrower_id INTEGER, FOREIGN KEY(borrower_id) REFERENCES borrower (borrower_id));"""
CREATE_BORROWER = """CREATE TABLE IF NOT EXISTS borrower
(borrower_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, debt INTEGER);"""
CREATE_PLACES = """CREATE TABLE IF NOT EXISTS places
(place_id SERIAL PRIMARY KEY, rack TEXT, shelf TEXT, book_id INTEGER, 
FOREIGN KEY(book_id) REFERENCES books (book_id)); """

INSERT_BOOK_RETURN_ID = """INSERT INTO books (title, author, date_release, is_borrow) 
VALUES (%s, %s, %s, %s) RETURNING book_id;"""
INSERT_BORROWER_RETURN_ID = """INSERT INTO borrower (first_name, last_name, email,
debt, book_id) VALUES (%s, %s, %s, %s, %s) RETURNING borrower_id;"""
INSERT_PLACE_RETURN_ID = """INSERT INTO places (rack, shelf, book_id) VALUES (%s, %s, %s)
RETURNING place_id;"""

SELECT_ALL_BOOKS = """SELECT * FROM books;"""
SELECT_BOOKS_BY_TITLE = """SELECT * FROM books WHERE title = %s;"""
SELECT_ALL_BORROWERS = """SELECT * FROM borrower ORDER BY borrower_id;"""
SELECT_BORROWERS_BY_NAME = """SELECT * FROM borrower WHERE first_name = %s AND last_name = %s;"""
SELECT_PLACE_BY_TITLE = """SELECT b.title, p.rack, p.shelf  FROM places AS p
INNER JOIN (SELECT * FROM books WHERE books.title = %s) as b 
ON p.book_id = b.book_id;"""
SELECT_FREE_BOOK = """SELECT books.book_id FROM books WHERE books.title = %s AND books.borrower_id is NULL LIMIT 1;"""
SELECT_BORROWERS_S_BOOKS = """SELECT borrower.borrower_id, borrower.first_name, COUNT(books.borrower_id = borrower.borrower_id)
AS amount_books FROM borrower INNER JOIN books ON books.borrower_id = borrower.borrower_id
WHERE borrower.borrower_id = %s GROUP BY borrower.borrower_id
ORDER BY borrower.borrower_id;"""
SELECT_BOOKS_BY_BORROWER_ID = """SELECT * FROM books WHERE books.borrower_id = 1
ORDER BY books.book_id;"""

DELETE_BOOK_BY_TITLE = """DELETE FROM books WHERE title=%s RETURNING*;"""
DELETE_BOOK_BY_ID = """DELETE FROM books WHERE book_id=%s RETURNING*;"""
DELETE_BORROWER_BY_NAME = """DELETE FROM borrower WHERE first_name = %s AND last_name = %s
RETURNING*;"""
DELETE_BORROWER_BY_ID = """DELETE FROM borrower WHERE borrower_id = %s RETURNING*; """

UPDATE_BOOKS_ID_BORROWER = """UPDATE books SET borrower_id = %s WHERE books.book_id = %s RETURNING books.book_id;"""
# UPDATE_BORROWER = """UPDATE borrower SET book_id = %s WHERE borrower.borrower_id = %s;"""
UPDATE_BOOKS_ID_IN_BORROWER = """UPDATE borrower SET book_id = %s WHERE borrower.borrower_id = %s;"""


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
            cursor.execute(CREATE_BORROWER)
            cursor.execute(CREATE_BOOKS)
            cursor.execute(CREATE_PLACES)

    def add_book(self, title, author, date_release, is_borrow):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_BOOK_RETURN_ID, (title, author, date_release, is_borrow))
            return cursor.fetchone()[0]

    def add_place(self, rack, shelf, book_id):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_PLACE_RETURN_ID, (rack, shelf, book_id))
            return cursor.fetchone()[0]

    def get_books(self):  # -> List["Books"]: dopkoncz to !!!
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_ALL_BOOKS)
            return cursor.fetchall()

    def get_books_by_title(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BOOKS_BY_TITLE, (title,))
            return cursor.fetchall()

    def get_books_by_borrower_id(self, borrower_id):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BOOKS_BY_BORROWER_ID, (borrower_id,))
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

    def remove_borrowers_by_id(self, id):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_BORROWER_BY_ID, (id,))
            return cursor.fetchall()[0]

    def find_book_place(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_PLACE_BY_TITLE, (title,))
            return cursor.fetchall()

    def check_free_book(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_FREE_BOOK, (title,))
            return cursor.fetchall()

    def borrow_book(self, id_borrower, id_book):
        with self.get_cursor() as cursor:
            cursor.execute(UPDATE_BOOKS_ID_BORROWER, (id_borrower, id_book))
            return cursor.fetchall()

    def borrower_s_books(self, id_borrower=1):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BORROWERS_S_BOOKS, (id_borrower,))
            return cursor.fetchall()[0]
