import sqlite3
from database import Database
from collections import namedtuple
from datetime import datetime
from borowers import get_borowers_by_return_date
import email
from dotenv import load_dotenv
from os import getenv
from emails import EmailSender, Credentials
from string import Template

load_dotenv()
connection = sqlite3.connect(getenv("DB_NAME"))

ssl_enable = getenv("SSL_ENABLE", False)
port = getenv("PORT")
smtp_serwer = getenv("SMTP_SERVER")
username = getenv("MAIL_USERNAME")
password = getenv("PASSWORD")

subject = getenv("SUBJECT")
sender = getenv("SENDER")
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


def send_reminder_to_borrower(borower):
    template = Template("""Hej $name,
    Masz moja ksiaze pt. $title.
    Data zwrotu minela $book_return_at
    """)

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
    print(f"Wysylam email do {borower.email}")


if __name__ == "__main__":
    borowers = get_borowers_by_return_date(connection, datetime.today().strftime("%Y-%m-%d"))
    with EmailSender(port, smtp_serwer, Credentials) as connection:
        for borower in borowers:
            send_reminder_to_borrower(borower)
