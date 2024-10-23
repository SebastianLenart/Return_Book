import pytest
import sqlite3
from borowers import get_borowers_by_return_date



@pytest.fixture
def create_connection():
    connection = sqlite3.connect(":memory:")  # nie trzeba robic commita
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS borows(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        book_title TEXT,
        book_return_at DATE)
        """)
    sample_data = [
        (1, "siostra","stentbike7@gmail.com", "ksiazka1", "2022-02-22"),
        (2, "brat", "seblentest@gmail.com", "ksiazka2", "2023-11-23")
    ]
    cursor.executemany("INSERT INTO borows VALUES (?, ?, ?, ?)", sample_data)
    return connection


def test_borowers(create_connection):
    users = get_borowers_by_return_date(create_connection, "2029-02-22")
    print(users)
    assert users[0].name == "siostra"
    assert users[1].name == "brat"
# python -m pytest -s borowers.py