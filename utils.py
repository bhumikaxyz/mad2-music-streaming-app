
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from application.models import Album



def csv_details(creator_id):
    albums = Album.query.filter_by(creator_id=creator_id).all()
    res=[]
    for album in albums:
        res.append((album.id,album.name,album.genre,album.artist_name,album.album_songs))

    return res

import os
from dotenv import load_dotenv
load_dotenv()

def send_email(to_address, subject, message):

    SMPTP_SERVER_HOST = 'smtp.gmail.com'
    SMPTP_SERVER_PORT = 587
    SENDER_ADDRESS = os.getenv('sender_email')
    SENDER_PASSWORD = os.getenv('email_app_password')
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To']=to_address
    msg['Subject'] = subject
    try:
        s = smtplib.SMTP(host=SMPTP_SERVER_HOST,port=SMPTP_SERVER_PORT)
        s.starttls()
        s.login(SENDER_ADDRESS,SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        print("mail sent")
        return True
    except Exception as e:
        print(e)
        return False
    

def get_users():
    from application.models import User
    users=User.query.all()
    res=[]
    for user in users:
        res.append(user.email)
    return res