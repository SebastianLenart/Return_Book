import sqlite3


def create_connection():
    with sqlite3.connect("baza.db") as connection:
        cursor = connection.cursor()
        return cursor


def get_author(cursor):
    cursor.execute("SELECT * FROM books WHERE author=?", ("autor2",))
    data = []
    for book in cursor.fetchall():
        data.append((book[0], book[1], book[2], book[3]))
        book_id, title, author, created_at = book
        # data.append({
        #         #     "title": title,
        #         #     "author": author
        #         # })

    return data


cursor = create_connection()
authors = get_author(cursor)
print(authors)
