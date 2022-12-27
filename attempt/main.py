import sqlite3
from database import Database
from collections import namedtuple
from datetime import datetime
from borowers import get_borowers_by_return_date
import email
from emails import EmailSender, Credentials

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
        id INTEGER PRIMNARY KEY AUTOINCREMENT,
        name TEXT,
        book_title TEXT,
        book_return_at DATE)
        """)


connection = sqlite3.connect("database1.db")

borowers = get_borowers_by_return_date(connection, datetime.today().strftime("%Y-%m-%d"))

with EmailSender(port, smtp_serwer, Credentials) as connection:
    message = email.message_from_string(f"""Oddaj ksiazke
    """)
    message.set_charset("utf-8")
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    connection.sendmail(sender, receiver, message)
