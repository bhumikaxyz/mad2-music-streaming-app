
from celery import Celery
from celery.schedules import crontab
import celery_config as celery_config

from application import app as flask_app

app = Celery()
app.conf.update(
        broker_url=celery_config.CELERY_BROKER_URL,
        result_backend=celery_config.CELERY_RESULT_BACKEND
    )

app.conf.timezone = "Asia/Kolkata"
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
    with flask_app.app_context():
        users = get_users()
    for user in users:
        
        send_email(user, "grocery app Monthly report", "this is monthly report")
    return "mail sent"

@app.task
def daily_remainder():
    with flask_app.app_context():
        users = get_users() 
        # users=["21f1007026@ds.study.iitm.ac.in"]
    for user in users:
        send_email(user, "Remainder to purchase ", "we have exciting offers , dont miss it")
    return "mail sent"



from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'schedules.daily_remainder',
        'schedule': crontab(hour=23, minute=3),
        # 'args': (16, 16),
    },
    'send-monthly-report': {
        'task': 'schedules.monthly_report',
        'schedule': crontab(hour=6,day_of_month=1)
        
       
    },
    'send-daily-reminder': {
        'task': 'schedules.daily_remainder',
        'schedule': crontab(hour=1,minute=45),
        
        
       
    },
    'send-every-39-seconds': {
        'task':'schedules.daily_remainder',
        'schedule': 30.0,
        
      
    
    
}
}

import csv, os
from utils import csv_details, get_users, send_email


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
