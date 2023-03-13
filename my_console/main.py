"""
Return book
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import psycopg2
from databasePS import Database
from models.book import Book
from models.borrower import Borrower
from models.emails import Email


class Menu:
    MENU = """---MENU---
    1.) List of books
    2.) Add a book
    3.) Remove a book
    4.) List of borrowers
    5.) Add a borrower
    6.) Remove a borrower
    7.) Find a book in library
    8.) Find borrower by first name and last name
    9.) Borrow a book
    10.) Return a book
    11.) Student's list of books
    12.) Check who doesn't return book in time and send mail to them
    14.) SPARE
    15.) Exit
    Enter your choice: """

    COST_OF_MONTH = 10  # when you exceed deadline every month

    def __init__(self):
        self.menu_options = {
            "1": self.list_of_books,
            "2": self.add_book,
            "3": self.remove_book,
            "4": self.list_of_borrowers,
            "5": self.add_borrower,
            "6": self.remove_borrower,
            "7": self.find_book,
            "8": self.find_borrower,
            "9": self.borrow_book,
            "10": self.return_book,
            "11": self.list_of_books_borrower,
            "12": self.check_deadline_exceeded
            # "13": self.send_mail_while_deadline_exceeded
        }
        self.today = datetime.today().date()

    def list_of_books(self, db):
        self.print_books_or_borrowers("List of books: ", Book.get_all(db))

    @staticmethod
    def print_books_or_borrowers(message, content, mode: int = 1):
        print(message)
        if len(content) == 0:
            print("Empty")
            return
        if mode == 1:  # books
            for book in content:
                print(str(book.book_id[0]) + ":", book.title[0],  # nie wiem cze is_borrow nie jest tupla ???!!!
                      book.author[0], book.date_release[0], book.borrower_id, book.rental_date[0], book.return_date)
        elif mode == 2:  # borrowers
            for borrower in content:
                print(str(borrower.borrower_id) + ":", borrower.first_name[0], borrower.last_name[0], borrower.email[0],
                      borrower.debt[0])

    @staticmethod
    def add_book(db):
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        date_release = input("Enter book date_release (DD-MM-YYYY): ")
        rack = input("Enter rack where is book: ")
        shelf = input("Enter shelf where is book: ")
        date_release = datetime.strptime(date_release, "%d-%m-%Y")
        date_release = date_release.strftime("%d-%m-%Y")
        rental_date = date_release
        return_date = date_release
        book = Book(title, author, date_release[:10], rack, shelf, rental_date=rental_date, return_date=return_date)
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
        borrower = Borrower.get_borrowers_by_name(db, first_name, last_name)
        if len(borrower) == 0:
            print("Not found borrower")
            return
        elif len(borrower) == 1:
            try:
                self.print_books_or_borrowers("Deleted borrower: ", Borrower.remove_borrower(db, first_name, last_name),
                                              2)
            except psycopg2.Error:
                print("You can't delete, because this borrower has a book! History has to be clear.")
        else:
            self.print_books_or_borrowers("List of borrower you want to delete: ",
                                          borrower, 2)
            borrower_id = input("Enter borrower's id you want to remove: ")
            try:
                self.print_books_or_borrowers("Deleted borrower: ",
                                              Borrower.remove_borrower(db, first_param=str(borrower_id),
                                                                       second_param=None,
                                                                       mode=2), 2)
            except psycopg2.Error:
                print("You can't delete, because this borrower has a book! History has to be clear.")

    @staticmethod
    def find_book(db):
        title = input("Enter the title book you want to find: ")
        data = Book.find_book(db, title)
        print(data)
        for tup in data:
            title, rack, shelf, borrower = tup
            print("Your book -", title, "rack:", rack, "shelf:", shelf, "borrower:", borrower)

    def find_borrower(self, db):
        first_name = input("Enter first name who you find: ")
        last_name = input("Enter last name who you find: ")
        self.print_books_or_borrowers("List of borrowers: ", Borrower.get_borrowers_by_name(db, first_name, last_name),
                                      2)

    def borrow_book(self, db):
        title_book = input("Enter title book: ")
        if len(Book.check_available_book(db, title_book)) == 0:
            print("This book is not available now.")
            return
        id_borrower = input("Enter id borrower: ")
        if (Book.check_available_book(db, title_book)[0] == Borrower.borrow_book(db, id_borrower, *
        Book.check_available_book(db, title_book)[0], self.today)[0]):
            print("OK")
        else:
            print("something it's wrong")
        self.student_list_of_books(db, id_borrower)

    def return_book(self, db):
        borrower_id = input("Enter your borrower_id: ")
        book_id = input("Enter book_id you want to return: ")
        return_book = Book.return_book(db, borrower_id, book_id, self.today)
        self.check_date_when_return_book(db, borrower_id, return_book[0]) # wyskakuje blad jak lista pusta! dodaj do Borrower moze
        self.print_books_or_borrowers("Return book is:", content=return_book)

    def list_of_books_borrower(self, db):
        id_borrower = input("Enter borrower id: ")
        self.student_list_of_books(db, id_borrower)

    def student_list_of_books(self, db, id_borrower):
        borrower_id, first_name, amount_of_books = db.borrower_s_books(id_borrower)
        print("ID borrower:", borrower_id, "First name:", first_name, "amount_of_books:", amount_of_books)
        self.print_books_or_borrowers(f"List of books:", content=Book.get_all_by_borrower_id(db, borrower_id))

    def check_deadline_exceeded(self, db):
        data = db.check_who_doesnt_return_book_in_time()
        for item in data:
            first_name, email, title, date_rental = item
            correct_delivery_date = date_rental + relativedelta(months=2)
            if correct_delivery_date < self.today:
                print("Deadline {} gone! Return book or extend the time.".format(correct_delivery_date), first_name,
                      email, title)
        self.send_mail_while_deadline_exceeded()

    def check_date_when_return_book(self, db, borrower_id, return_book):
        # print("rental_date:", str(return_book.rental_date[0]), "return_date:", str(return_book.return_date))
        delta_date = return_book.return_date - return_book.rental_date[0]
        if delta_date > timedelta(days=60):
            delta_date = delta_date - timedelta(days=60)
            constans_every_month = int((int(delta_date.days) / 30) + 1)
            print("constans_every_month: ", constans_every_month, "delta_time:", delta_date)
            if constans_every_month >= 2:
                cost_borrower_book = self.COST_OF_MONTH * constans_every_month
            else:
                cost_borrower_book = self.COST_OF_MONTH
            actual_debt = Borrower.get_debt_by_borrower_id(db, borrower_id)
            actual_debt = actual_debt - cost_borrower_book
            Borrower.set_debt(db, actual_debt, borrower_id)
            print("debt after:", actual_debt)

    def send_mail_while_deadline_exceeded(self):
        with Email() as serwer:
            serwer.send_test_mail()

    def start(self):
        with Database() as db:
            db.create_tables()

        while (selection := input(self.MENU)) != "14":
            try:
                self.menu_options[selection](db)
            except KeyError:
                print("Invalid key in dictionary")


if __name__ == "__main__":
    app = Menu()
    app.start()
