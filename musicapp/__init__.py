import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from sqlalchemy.sql import func 
from flask_cors import CORS
from flask_security import Security


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .sec import datastore
app.security = Security(app, datastore)


# from musicapp.models import User, Song, Album, Artist, Playlist, Interactions

from musicapp.resources import api
api.init_app(app)

from musicapp import views



