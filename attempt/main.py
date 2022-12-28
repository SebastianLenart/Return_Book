import sqlite3
from database import Database
from collections import namedtuple
from datetime import datetime
from borowers import get_borowers_by_return_date
import email
from emails import EmailSender, Credentials
from string import Template

ssl_enable = False
port = 2525
smtp_serwer = "smtp.mailtrap.io"
username = "2e1cea1609e7ab"
password = "abe1005125a3ee"

subject = "Oddaj ksiazke2"
sender = "Seba Lenart <stentbike7@gmail.com>"
receiver = "Seba Lenart <seblentest@gmail.com>"
Credentials = Credentials(username, password)


# https://mailtrap.io/inboxes/2027163/messages/3203073128


def setup(connection):
    with Database(connection) as database:
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS borows(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
        book_title TEXT,
        book_return_at DATE)
        """)


connection = sqlite3.connect("database1.db")

borowers = get_borowers_by_return_date(connection, datetime.today().strftime("%Y-%m-%d"))
template = Template("""Hej $name,
Masz moja ksiaze pt. $title.
Data zwrotu minela $book_return_at
""")
with EmailSender(port, smtp_serwer, Credentials) as connection:
    for borower in borowers:
        text = template.substitute({
            "name": borower.name,
            "title": borower.book_title,
            "book_return_at": borower.book_return_at})
        message = email.message_from_string(text)
        message.set_charset("utf-8")
        message["From"] = sender
        message["To"] = borower.email
        message["Subject"] = "Oddaj"

        connection.sendmail(sender, borower.email, message)
