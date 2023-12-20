import time
from celery import Celery
from celery.schedules import crontab
# from routes import send_email
import celery_config as celery_config


# celery is used for two purposes
   # to do background tasks
    # to schedule tasks

# what is a background task?
    # a task that runs in the background without blocking the main thread
    # ex: sending email, generating pdf, sending sms, etc
#
from application import app as flask_app

print("broker",celery_config.CELERY_BROKER_URL)
print("result",celery_config.CELERY_RESULT_BACKEND)

app = Celery()
app.conf.update(
        broker_url=celery_config.CELERY_BROKER_URL,
        result_backend=celery_config.CELERY_RESULT_BACKEND
    )

app.conf.timezone = "Asia/kolkata"
app.conf.broker_connection_retry_on_startup=True

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=17, minute=30, day_of_week=0),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)


from jinja2 import Template

@app.task
def monthly_report():
    from model  import User
    with flask_app.app_context():
        users = User.query.all()
    for user in users:
        with open('test.html', 'r') as f:
            if user.roles[0].name == 'user':    
                template = Template(f.read())
                send_email(user.email, "grocery app Monthly report", template.render(email=user.email,name=user.user_name),content='html',attachement_file=None)
    return "mail sent"

@app.task
def daily_report():
    from model  import User,Role
    from model import db
    from utils import get_users
    with flask_app.app_context():
        users = get_users()
    print("ssssssss", users)
    
    for user in users:
        
        with open('test.html', 'r') as f:
                if user[1]== 'user':
                    template = Template(f.read())
                    send_email(user[0], "grocery app Daily remainder gokul", "remainder to buy groceries", content='text', attachment_file=None)
    return "mail sent"



from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'schedules.add',
        'schedule': crontab(hour=17, minute=16),
        'args': (16, 16),
    },
    'send-monthly-report': {
        'task': 'schedules.monthly_report',
        'schedule': crontab(hour=9,day_of_month=1)
        
       
    },
    'send-daily-reminder': {
        'task': 'schedules.daily_report',
        'schedule': crontab(hour=1,minute=45),
        
        
       
    },
    'send-every-10-seconds': {
        'task':'schedules.daily_report',
        'schedule': 30.0,
        
      
    
    
}
}

import csv, os
from utils import csv_details


@app.task
def create_csv(user_id):
    # time.sleep(25)
    with open(f'export1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id","name","genre","artist_name","album_songs" ])
        with flask_app.app_context():
            result = csv_details(user_id)
        for row in result:
            data=[row[0],row[1],row[2],row[3],row[4]]
            writer.writerow(data)  # to send file to user as download

    
    return "export.csv"
