"""
Return book

"""
from databasePS import Database


class Menu():
    MENU = """---MENU---
    1.) List of books
    2.) Add/Remove book
    3.) List of borrowers
    4.) Add/Remove borower
    5.) Find a book by ..
    6.) Find borower by ..
    7.) Borrow a book
    8.) Return a book
    9.) Exit
    Enter your choice: """

    def __init__(self):
        self.menu_options = {
            "1": self.list_of_books
        }

    def list_of_books(self, db):
        pass

    def start(self):
        with Database() as db:
            db.create_tables()

        while (selection := input(self.MENU)) != "9":
            try:
                self.menu_options[selection](db)
            except KeyError:
                print("Invalid key in dictionary")


if __name__ == "__main__":
    app = Menu()
    app.start()
