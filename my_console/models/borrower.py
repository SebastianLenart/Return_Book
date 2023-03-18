class Borrower:
    def __init__(self, first_name: str, last_name: str, email: str, debt: int = 0,
                 borrower_id: int = None):
        self.first_name = first_name,
        self.last_name = last_name,
        self.email = email,
        self.debt = debt,
        self.borrower_id = borrower_id

    def save(self, db):
        self.borrower_id = db.add_borrower(self.first_name, self.last_name, self.email, self.debt)

    @classmethod
    def get_all_borrowers(cls, db):
        return [cls(borrower[1], borrower[2], borrower[3], borrower[4],
                    borrower[0]) for borrower in db.get_all_borrowers()]

    @classmethod
    def get_borrowers_by_name(cls, db, fname, lname):
        return [cls(borrower[1], borrower[2], borrower[3], borrower[4],
                    borrower[0]) for borrower in db.get_borrowers_by_name(fname, lname)]

    @classmethod
    def remove_borrower(cls, db, first_param: str = None, second_param: str = None, mode: int = 1):
        return_borrower = None
        if mode == 1:
            return_borrower = db.remove_borrowers_by_name(first_param, second_param)
        elif mode == 2:
            return_borrower = db.remove_borrowers_by_id(first_param)
        return [cls(return_borrower[1], return_borrower[2], return_borrower[3], return_borrower[4],
                    return_borrower[0])]

    @staticmethod
    def borrow_book(db, id_borrower, id_book, date_rental):
        print(db.borrow_book(id_borrower, id_book, date_rental))
        return db.borrow_book(id_borrower, id_book, date_rental)

    @staticmethod
    def get_debt_by_borrower_id(db, id_borrower):
        return db.get_debt_by_borrower_id(id_borrower)

    @staticmethod
    def set_debt(db, money, id_borrower):
        db.set_new_value_debt(money, id_borrower) # moze cos zwrocic ???
