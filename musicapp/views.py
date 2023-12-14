from flask import render_template, url_for, flash, redirect, request, abort
from musicapp import app
from flask_security import current_user
from mutagen.mp3 import MP3

@app.route('/')
def layout():
    return render_template('layout.html')