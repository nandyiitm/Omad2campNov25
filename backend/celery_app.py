from celery import Celery


# init Celery app
celeryApp = Celery(
    'tasks',
    broker = 'redis://localhost:6379/0'
)

# config
celeryApp.conf.update(
    timezome='Asia/Kolkata',
    enable_utc=False
)

from app import app
from models import User
from mail import send_mail

@celeryApp.task()
def daily_reminders():
    with app.app_context():
        for user in User.query.all():
            subject = "Hey there?"
            mail_template = f"""
<h1>Hey {user.name}</h1>
<p>For got to visit our application?</p>
<a href='http://localhost:5173'>Click here to visit</a>
"""
            send_mail(str(user.email), subject, mail_template)
    return "Sent Daily Reminders!"

@celeryApp.task()
def export_csv():

    with app.app_context():

        users = User.query.all()
        users = [{'name': user.name, 'email': user.email} for user in users]

        import csv

        with open('static/report.csv', mode='w', newline='') as f:
            import time
            time.sleep(10)
            writer = csv.DictWriter(f, fieldnames=users[0].keys())
            writer.writeheader()
            writer.writerows(users)

        send_mail('admin@gmail.com', 'Rport Ready!', '<a href=\"http://127.0.0.1:5000/static/report.csv\">Download Report</a>')



# scheduled tasks
from celery.schedules import crontab
import datetime

celeryApp.conf.beat_schedule = {
    "daily_reminders": {
        'task': 'celery_app.daily_reminders',
        # 'schedule': crontab(minute=23, hour=20),
        'schedule': datetime.timedelta(seconds=3)
    }
}