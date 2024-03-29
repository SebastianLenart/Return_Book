import pytest
from main2 import get_author
import sqlite3

@pytest.fixture()
def create_data_base():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE books
    (id integer, title text, author text, created_at date)""")
    sample_data = [
        (1, "ksiazka1", "autor2", "2020-01-02 13:00:01"),
        (2, "ksiazka2", "autor3", "2020-01-03 13:00:01"),
    ]
    cursor.executemany("INSERT INTO books VALUES (?, ?, ?,?)", sample_data)
    return cursor


def test_get_author(create_data_base):
    cursor = create_data_base
    data = get_author(cursor)
    assert data[0] == (1, "ksiazka1", "autor2", "2020-01-02 13:00:01")

# python -m pytest -s main2_test.py