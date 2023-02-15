from datetime import datetime


class Book:
    def __init__(self, title: str, author: str, date_release: str, rack: str, shelf: str,
                 borrower_id: int = None, book_id: int = None):
        self.book_id = book_id,
        self.title = title,
        self.author = author,
        self.date_release = date_release,
        self.borrower_id = borrower_id
        self.rack = rack,
        self.shelf = shelf
        self.place_id = None

    def save(self, db):
        self.book_id = db.add_book(self.title, self.author, self.date_release, self.is_borrow)
        self.place_id = db.add_place(self.rack, self.shelf, self.book_id)

    @classmethod
    def get_all(cls, db):
        books = db.get_books()
        return [cls(book[1], book[2], book[3], book[4], book[0]) for book in books]

    @classmethod
    def get_all_by_title(cls, db, title):
        books = db.get_books_by_title(title)
        return [cls(book[1], book[2], book[3], book[4], book[0]) for book in books]

    @classmethod
    def remove_book(cls, db, item, mode: int = 1):
        return_book = None
        if mode == 1:
            return_book = db.remove_book_by_title(item)
        elif mode == 2:
            return_book = db.remove_book_by_id(item)
            print(return_book)

        return [cls(return_book[1], return_book[2], return_book[3],
                    return_book[4], return_book[0])]

    @staticmethod
    def find_book(db, title) -> list:
        return db.find_book_place(title)

    @staticmethod
    def check_available_book(db, title):
        return db.check_free_book(title)
