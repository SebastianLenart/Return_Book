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
            "2": self.add_book
        }

    def list_of_books(self, db):
        print("List of books:")
        for book in Book.get_all(db):
            print(str(book.book_id[0])+":", book.title[0], # nie wiem cze is_borrow nie jest tupla ???!!!
                  book.author[0], book.date_release[0], book.is_borrow)

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
