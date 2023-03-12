import smtplib, ssl
from dotenv import load_dotenv
from os import getenv
from email.message import EmailMessage

print("dsd")
load_dotenv()

def send_mail():
    smtp_serwer = "smtp.gmail.com"
    port = 465
    sender_email = getenv("EMAIL")
    password = getenv("PASSWORD") # generuje sie w ustawieniach google

    msg = EmailMessage()
    msg['Subject'] = "subject"
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg.set_content("Text")

    message = """\
    Subject: Hi there

    This message is sent from Python."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_serwer, port, context=context) as serwer:
        serwer.login(sender_email, password)
        serwer.sendmail(sender_email, sender_email, message)
        serwer.send_message(msg) # z subject i z text oddzielnie

send_mail()