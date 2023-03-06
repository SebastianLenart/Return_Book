import smtplib, ssl

print("dsd")


def send_mail():
    smtp_serwer = "smtp.gmail.com"
    port = 465
    sender_email = "seblentest@gmail.com"
    password = "lsqajzywpgkrawog"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_serwer, port, context=context) as serwer:
        serwer.login(sender_email, password)
        serwer.sendmail(sender_email, sender_email, "testowy mail")
1