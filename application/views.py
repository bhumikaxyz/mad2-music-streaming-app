from flask import render_template, url_for, flash, redirect, request, abort
from application import app
from flask_security import current_user
from mutagen.mp3 import MP3

@app.route('/')
def index():
    return render_template("index.html")