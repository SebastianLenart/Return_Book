class Borrower:
    def __init__(self, first_name: str, last_name: str, email: str, debt: int = 0, book_id: int = None,
                 borrower_id: int = None):
        self.first_name = first_name,
        self.last_name = last_name,
        self.email = email,
        self.debt = debt,
        self.book_id = book_id,
        self.borrower_id = borrower_id

    def save(self, db):
        self.borrower_id = db.add_borrower(self.first_name, self.last_name, self.email, self.debt, self.book_id)

    @classmethod
    def get_all_borrowers(cls, db):
        return [cls(borrower[1], borrower[2], borrower[3], borrower[4],
                    borrower[5], borrower[0]) for borrower in db.get_all_borrowers()]

    @classmethod
    def get_borrowers_by_name(cls, db, fname, lname):
        return [cls(borrower[1], borrower[2], borrower[3], borrower[4],
                    borrower[5], borrower[0]) for borrower in db.get_borrowers_by_name(fname, lname)]

    @classmethod
    def remove_borrower(cls, db, first_param: str = None, second_param: str = None, mode: int = 1):
        return_borrower = None
        if mode == 1:
            return_borrower = db.remove_borrowers_by_name(first_param, second_param)
        elif mode == 2:
            return_borrower = db.remove_borrowers_by_id(first_param)
        return [cls(return_borrower[1], return_borrower[2], return_borrower[3], return_borrower[4],
                    return_borrower[5], return_borrower[0])]
