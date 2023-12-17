import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from sqlalchemy.sql import func 
from flask_cors import CORS
from flask_security import Security
from flask_jwt_extended import JWTManager


app = Flask(__name__, template_folder='templates')
CORS(app)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from .sec import datastore
# app.security = Security(app, datastore)


# from application.models import User, Song, Album, Artist, Playlist, Interactions

jwt = JWTManager(app)

from application.resources import api
api.init_app(app)



from application import views



