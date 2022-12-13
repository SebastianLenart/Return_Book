import sqlite3


def create_connection():
    with sqlite3.connect("baza.db") as connection:
        cursor = connection.cursor()
        return cursor


def get_author(cursor):
    cursor.execute("SELECT * FROM books WHERE author=?", ("autor4",))
    data = []
    for book in cursor.fetchall():
        book_id, title, author, created_at = book
        data.append({
            "title": title,
            "author": author
        })
    return data


cursor = create_connection()
authors = get_author(cursor)
print(authors)
