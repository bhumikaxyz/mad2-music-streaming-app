from application import app, db
from flask import render_template
from application.models import User, Role
# from application.sec import datastore
# from flask_security.utils import get_random_token


with app.app_context():
    db.create_all()

# @app.route('/')
# def index():
#     app.logger.debug("hiiii")
#     return render_template("index.html")
   
if __name__ == '__main__':
    app.run(debug = True) 



