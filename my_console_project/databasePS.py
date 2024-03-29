from contextlib import contextmanager
from pprint import pprint

from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from configparser import ConfigParser
from psycopg2.pool import SimpleConnectionPool

CREATE_BOOKS = """CREATE TABLE IF NOT EXISTS books
(book_id SERIAL PRIMARY KEY, title TEXT, author TEXT, date_release TEXT,
borrower_id INTEGER, rental_date DATE, return_date DATE, FOREIGN KEY(borrower_id) REFERENCES borrower (borrower_id));"""
CREATE_BORROWER = """CREATE TABLE IF NOT EXISTS borrower
(borrower_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, debt INTEGER);"""
CREATE_PLACES = """CREATE TABLE IF NOT EXISTS places
(place_id SERIAL PRIMARY KEY, rack TEXT, shelf TEXT, book_id INTEGER, 
FOREIGN KEY(book_id) REFERENCES books (book_id)); """

INSERT_BOOK_RETURN_ID = """INSERT INTO books (title, author, date_release, borrower_id, rental_date, return_date) 
VALUES (%s, %s, %s, %s, %s, %s) RETURNING book_id;"""
INSERT_BORROWER_RETURN_ID = """INSERT INTO borrower (first_name, last_name, email,
debt) VALUES (%s, %s, %s, %s) RETURNING borrower_id;"""
INSERT_PLACE_RETURN_ID = """INSERT INTO places (rack, shelf, book_id) VALUES (%s, %s, %s)
RETURNING place_id;"""

SELECT_ALL_BOOKS = """SELECT * FROM books ORDER BY books.book_id;"""
# SELECT_BOOK_ID_BY_TITLE = """SELECT books.book_id FROM books WHERE books.title = %s ORDER BY books.book_id LIMIT 1;"""
SELECT_ALL_PLACES = """SELECT * FROM places ORDER BY places.book_id;"""
SELECT_BOOKS_BY_TITLE = """SELECT * FROM books WHERE title = %s ORDER BY books.book_id;"""
SELECT_ALL_BORROWERS = """SELECT * FROM borrower ORDER BY borrower_id;"""
SELECT_BORROWERS_BY_NAME = """SELECT * FROM borrower WHERE first_name = %s AND last_name = %s 
ORDER BY borrower.borrower_id;"""
SELECT_PLACE_BY_TITLE = """SELECT b.title, p.rack, p.shelf, borrower.first_name  || ' ' || borrower.last_name as "Full name"  
FROM places AS p INNER JOIN (SELECT * FROM books WHERE books.title = %s) as b 
ON p.book_id = b.book_id
left join borrower on borrower.borrower_id = b.borrower_id;"""
SELECT_FREE_BOOK = """SELECT books.book_id FROM books WHERE books.title = %s AND books.borrower_id is NULL LIMIT 1;"""
SELECT_BORROWERS_S_BOOKS = """SELECT borrower.borrower_id, borrower.first_name, COUNT(books.borrower_id = borrower.borrower_id)
AS amount_books FROM borrower INNER JOIN books ON books.borrower_id = borrower.borrower_id
WHERE borrower.borrower_id = %s GROUP BY borrower.borrower_id
ORDER BY borrower.borrower_id;"""
SELECT_BOOKS_BY_BORROWER_ID = """SELECT * FROM books WHERE books.borrower_id = %s
ORDER BY books.book_id;"""
SELECT_PLACE_BY_BORROWER_ID = """SELECT places.place_id, places.rack, places.shelf FROM places
INNER JOIN books ON books.book_id = places.book_id WHERE books.borrower_id = %s ORDER BY books.book_id;"""
SELECT_PLACE_BY_BOOK_TITLE = """SELECT places.place_id, places.rack, places.shelf FROM places
INNER JOIN books ON books.book_id = places.book_id WHERE books.title = %s ORDER BY books.book_id;"""
SELECT_PLACE_BY_BOOK_ID = """SELECT places.place_id, places.rack, places.shelf FROM places
INNER JOIN books ON books.book_id = places.book_id WHERE books.book_id = %s ORDER BY books.book_id;"""
SELECT_WHO_DOESNT_RETURN_BOOK = """SELECT borrower.first_name, borrower.email, books.title, books.rental_date  
FROM books INNER JOIN borrower ON books.borrower_id = borrower.borrower_id
WHERE books.return_date IS NULL AND books.borrower_id IS NOT NULL;"""
SELECT_DEBT_BY_BORROWER_ID = """SELECT borrower.debt FROM borrower WHERE borrower.borrower_id = %s;"""

DELETE_BOOK_BY_TITLE = """DELETE FROM books WHERE title=%s RETURNING*;"""
DELETE_BOOK_BY_ID = """DELETE FROM books WHERE book_id=%s RETURNING*;"""
DELETE_BORROWER_BY_NAME = """DELETE FROM borrower WHERE first_name = %s AND last_name = %s
RETURNING*;"""
DELETE_BORROWER_BY_ID = """DELETE FROM borrower WHERE borrower_id = %s RETURNING*; """
DELETE_PLACE_BY_BOOK_ID = """DELETE FROM places WHERE book_id = %s;"""

UPDATE_BOOKS_ID_BORROWER = """UPDATE books SET borrower_id = %s, rental_date = %s,  return_date = NULL
WHERE books.book_id = %s RETURNING books.book_id;"""
RETURN_BOOK = """UPDATE books SET borrower_id = NULL, return_date = %s WHERE borrower_id = %s AND books.book_id = %s 
RETURNING *;"""
# UPDATE_BORROWER = """UPDATE borrower SET book_id = %s WHERE borrower.borrower_id = %s;"""
UPDATE_BOOKS_ID_IN_BORROWER = """UPDATE borrower SET book_id = %s WHERE borrower.borrower_id = %s;"""
UPDATE_DEBT = """UPDATE borrower SET debt = %s WHERE borrower_id = %s;"""
UPDATE_DATES_IN_BOOKS = """UPDATE books SET rental_date = NULL, return_date = NULL WHERE book_id = %s AND
borrower_id is NULL;"""

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

    def add_book(self, title, author, date_release, borrower_id, rental_date, return_date):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_BOOK_RETURN_ID, (title, author, date_release, borrower_id, rental_date, return_date))
            return cursor.fetchone()[0]

    def add_place(self, rack, shelf, book_id):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_PLACE_RETURN_ID, (rack, shelf, book_id))
            return cursor.fetchone()[0]

    def get_books(self):  # -> List["Books"]: dopkoncz to !!!
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_ALL_BOOKS)
            return cursor.fetchall()

    def get_places(self):  # -> List["Books"]: dopkoncz to !!!
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_ALL_PLACES)
            return cursor.fetchall()

    def get_books_by_title(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BOOKS_BY_TITLE, (title,))
            return cursor.fetchall()

    def get_books_by_borrower_id(self, borrower_id):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BOOKS_BY_BORROWER_ID, (borrower_id,))
            return cursor.fetchall()

    def get_places_book_by_borrower_id(self, borrower_id):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_PLACE_BY_BORROWER_ID, (borrower_id,))
            return cursor.fetchall()

    def get_places_book_by_title_book(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_PLACE_BY_BOOK_TITLE, (title,))
            return cursor.fetchall()

    def get_place_book_by_book_id(self, book_id):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_PLACE_BY_BOOK_ID, (book_id,))
            return cursor.fetchall()

    def remove_book_by_title(self, title):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_BOOK_BY_TITLE, (title,))
            return cursor.fetchall()[0]

    def remove_book_by_id(self, id):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_BOOK_BY_ID, (id,))
            return cursor.fetchall()[0]

    def remove_place_by_book_id(self, book_id):
        with self.get_cursor() as cursor:
            cursor.execute(DELETE_PLACE_BY_BOOK_ID, (book_id,))

    def add_borrower(self, first_name, last_name, email, debt):
        with self.get_cursor() as cursor:
            cursor.execute(INSERT_BORROWER_RETURN_ID, (first_name, last_name, email, debt))
            return cursor.fetchone()[0]

    def get_all_borrowers(self):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_ALL_BORROWERS)
            return cursor.fetchall()

    def get_borrowers_by_name(self, fname, lname):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BORROWERS_BY_NAME, (fname, lname))
            return cursor.fetchall()

    def get_debt_by_borrower_id(self, id_borrower):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_DEBT_BY_BORROWER_ID, (id_borrower, ))
            return cursor.fetchall()[0][0]

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

    def borrow_book(self, id_borrower, id_book, date_rental):
        with self.get_cursor() as cursor:
            cursor.execute(UPDATE_BOOKS_ID_BORROWER, (id_borrower, date_rental, id_book))
            return cursor.fetchall()

    def borrower_s_books(self, id_borrower=1):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_BORROWERS_S_BOOKS, (id_borrower,))
            return cursor.fetchall()[0]

    def return_book(self, borrower_id, book_id, date_return):
        with self.get_cursor() as cursor:
            cursor.execute(RETURN_BOOK, (date_return, borrower_id, book_id))
            return cursor.fetchall()

    def get_rentaldate_who_doesnt_return_book(self):
        with self.get_cursor() as cursor:
            cursor.execute(SELECT_WHO_DOESNT_RETURN_BOOK)
            return cursor.fetchall()

    def set_new_value_debt(self, money, borrower_id):
        with self.get_cursor() as cursor:
            cursor.execute(UPDATE_DEBT, (money, borrower_id))

    def update_dates_from_books(self, book_id):
        with self.get_cursor() as cursor:
            cursor.execute(UPDATE_DATES_IN_BOOKS, (book_id,))