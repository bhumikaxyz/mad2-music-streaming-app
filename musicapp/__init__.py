import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from musicapp.config import Config
from sqlalchemy.sql import func 
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from musicapp import routes
# from musicapp.models import User, Song, Album, Artist, Playlist, Interactions

from musicapp.resources import api
api.init_app(app)






