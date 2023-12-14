from musicapp import app, db
from flask import render_template

with app.app_context():
    db.create_all()


# @app.route('/')
# def layout():
#     return render_template('layout.html')
   
if __name__ == '__main__':
    app.run(debug = True) 



