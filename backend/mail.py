import smtplib
from email.mime.text import MIMEText

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_EMAIL = 'admin@gmail.com'

def send_mail(to, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)

if __name__ == '__main__':

    # for testing mails
    from app import app
    from models import User

    with app.app_context():
        for user in User.query.all():

            send_mail(str(user.email), 'Test email', f'<h1>Hey {user.name}!</h1><p>Just checking</p>')

    print('sent mails')