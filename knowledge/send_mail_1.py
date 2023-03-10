import smtplib, ssl
from dotenv import load_dotenv
from os import getenv

print("dsd")
load_dotenv()

def send_mail():
    smtp_serwer = "smtp.gmail.com"
    port = 465
    sender_email = getenv("EMAIL")
    password = getenv("PASSWORD") # generuje sie w ustawieniach google
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_serwer, port, context=context) as serwer:
        serwer.login(sender_email, password)
        serwer.sendmail(sender_email, sender_email, "testowy mail")

send_mail()