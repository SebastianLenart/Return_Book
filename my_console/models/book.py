from datetime import datetime


class Book:
    def __init__(self, title: str, author: str, date_release, is_borrow: str, book_id: int=None ):
        self.book_id = book_id,
        self.title = title,
        self.author = author,
        self.date_release = date_release,
        self.is_borrow = is_borrow

    def save(self, db):
        pass