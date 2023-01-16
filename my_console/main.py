"""
Return book

"""
from databasePS import Database


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
            "1": self.list_of_books
        }

    def list_of_books(self, db):
        pass

    def add_book(self):
        pass

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
