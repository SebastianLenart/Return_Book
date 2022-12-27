from unittest.mock import patch
from send_mail_1 import send_mail

@patch("smtplib.SMTP_SSL")
def test_send_mail(mock_smtp):
    send_mail()
    mock_smtp.assert_called()
    # mock_smtp.return_value to instancja
    context = mock_smtp.return_value.__enter__.return_value
    context.login.assert_called()
    context.sendmail.assert_called_with('seblentest@gmail.com', 'seblentest@gmail.com', 'testowy mail')
