import smtplib
import ssl
from dotenv import load_dotenv
from os import getenv
from email.message import EmailMessage


class Email(smtplib.SMTP_SSL):

    def __init__(self):
        load_dotenv()
        self.port = 465
        self.smtp_serwer = 'smtp.gmail.com'
        self.sender_email = getenv("MAIL_USERNAME")
        self.password = getenv("PASSWORD")  # generuje sie w ustawieniach google
        self.msg = EmailMessage()
        self.msg['Subject'] = "subject"
        self.msg['From'] = self.sender_email
        self.msg['To'] = self.sender_email
        self.msg.set_content("Text")
        self.context = ssl.create_default_context()
        smtplib.SMTP_SSL.__init__(self, host=self.smtp_serwer, port=self.port, context=self.context)

    def __enter__(self):
        self.login(self.sender_email, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, Exception):
            print(exc_type, exc_val, exc_tb)
            self.close()

    def send_mail(self, receivers, subject, message):
        self.msg['To'] = receivers
        self.msg['Subject'] = subject
        self.msg.set_content(message)
        self.send_message(self.msg)

    def send_test_mail(self):
        self.send_message(self.msg)

