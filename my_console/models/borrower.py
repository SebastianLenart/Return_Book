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
        return [cls(borrower.first_name, borrower.last_name, borrower.email, borrower.debt,
                    borrower.book_id, borrower.borrower_id) for borrower in db.get_all_borrowers()]
