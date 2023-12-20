from application import app, db
from flask import render_template
from application.models import User, Role
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# from application.sec import datastore
# from flask_security.utils import get_random_token
from app_cache import cache
from worker import celery_init_app
with app.app_context():
    db.create_all()

celery_app = celery_init_app(app)
cache.init_app(app)
# @app.route('/')
# def index():
#     app.logger.debug("hiiii")
#     return render_template("index.html")

from schedules import create_csv
from flask import jsonify
# @app.get('/download-csv')
# def csv_download():
#     import time 
#     task = create_csv.delay()
#     return jsonify({"task-id": task.id})   


@app.route('/download-csv')
# @jwt_required()
def export_csv():
    current_user_id = 1
    from schedules import create_csv
    task=create_csv.apply_async(args=[current_user_id])
    print("current_user_id", current_user_id)
    # return "DSasd"
    return jsonify({"task_id":task.id}), 200

@app.route('/get-csv/<task_id>')
def get_csv(task_id):
    from celery.result import AsyncResult
    from schedules import create_csv
    from flask import send_file
    task=create_csv.AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({"task_state":task.state}), 200
    elif task.state == 'SUCCESS':
        return send_file(f'../export1.csv', as_attachment=True)
    else:
        return jsonify({"task_state":task.state}), 200



if __name__ == '__main__':
    app.run(debug = True) 



