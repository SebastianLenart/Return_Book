"""
Return book
"""
from datetime import datetime
from databasePS import Database
from models.book import Book
from models.borrower import Borrower


class Menu():
    MENU = """---MENU---
    1.) List of books
    2.) Add a book
    3.) Remove a book
    4.) List of borrowers
    5.) Add a borrower
    6.) Remove a borrower
    7.) Find a book by ..
    8.) Find borower by ..
    9.) Borrow a book
    10.) Return a book
    11.) Exit
    Enter your choice: """

    def __init__(self):
        self.menu_options = {
            "1": self.list_of_books,
            "2": self.add_book,
            "3": self.remove_book,
            "4": self.list_of_borrowers,
            "5": self.add_borrower,
            "6": self.remove_borrower
        }

    def list_of_books(self, db):
        self.print_books_or_borrowers("List of books: ", Book.get_all(db))

    @staticmethod
    def print_books_or_borrowers(message, content, mode: int = 1):
        print(message)
        if mode == 1:  # books
            for book in content:
                print(str(book.book_id[0]) + ":", book.title[0],  # nie wiem cze is_borrow nie jest tupla ???!!!
                      book.author[0], book.date_release[0], book.is_borrow)
        elif mode == 2:  # borrowers
            for borrower in content:
                print(str(borrower.borrower_id) + ":", borrower.first_name[0], borrower.last_name[0], borrower.email[0],
                      borrower.debt[0], borrower.book_id[0])

    @staticmethod
    def add_book(self, db):
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        date_release = input("Enter book date_release (DD-MM-YYYY): ")
        date_release = datetime.strptime(date_release, "%d-%m-%Y")
        date_release = date_release.strftime("%d-%m-%Y")
        print(date_release[:10], type(date_release))
        book = Book(title, author, date_release[:10])
        book.save(db)

    def remove_book(self, db):
        title = input("Enter book title you want to remove: ")
        if len(Book.get_all_by_title(db, title)) == 0:
            print("Not found this book")
            return
        elif len(Book.get_all_by_title(db, title)) == 1:
            self.print_books_or_borrowers("Deleted book: ", Book.remove_book(db, title))
            return
        else:
            self.print_books_or_borrowers("List of books you want to delete: ", Book.get_all_by_title(db, title))
            id = input("Enter book's id you want to remove: ")
            self.print_books_or_borrowers("Deleted book: ", Book.remove_book(db, id, 2))

    def list_of_borrowers(self, db):
        self.print_books_or_borrowers("List of borrowers: ", Borrower.get_all_borrowers(db), 2)

    @staticmethod
    def add_borrower(db):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        Borrower(first_name, last_name, email).save(db)

    def remove_borrower(self, db):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        if len(Borrower.get_borrowers_by_name(db, first_name, last_name)) == 0:
            print("Not found borrower")
            return
        elif len(Borrower.get_borrowers_by_name(db, first_name, last_name)) == 1:
            self.print_books_or_borrowers("Deleted borrower: ", Borrower.remove_borrower(db, first_name, last_name), 2)
        else:
            self.print_books_or_borrowers("List of borrower you want to delete: ",
                                          Borrower.get_borrowers_by_name(db, first_name, last_name), 2)
            id = input("Enter borrower's id you want to remove: ")
            self.print_books_or_borrowers("Deleted borrower: ",
                                          Borrower.remove_borrower(db, first_param=str(id), second_param=None, mode=2), 2)

    def start(self):
        with Database() as db:
            db.create_tables()

        while (selection := input(self.MENU)) != "11":
            try:
                self.menu_options[selection](db)
            except KeyError:
                print("Invalid key in dictionary")


if __name__ == "__main__":
    app = Menu()
    app.start()
