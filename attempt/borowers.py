from database import Database
from collections import namedtuple

Entity = namedtuple("Entity", " name, book_title book_return_at")


def get_borowers_by_return_date(connection, book_return_at):
    entities = []
    with Database(connection) as database:
        database.cursor.execute("""
        SELECT name, book_title, book_return_at FROM borows
        WHERE book_return_at <= ?
        """, (book_return_at,))

        for name, book_title, book_return_at in database.cursor.fetchall():
            entities.append(Entity(name, book_title, book_return_at))
    return entities
