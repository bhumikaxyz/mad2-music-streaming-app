from application import db, app
from application.models import *

with app.app_context():
    role_1 = Role(name='admin', description='Admin')
    role_2 = Role(name='creator', description='Creator')
    role_3 = Role(name='user', description='User')


    user = User.query.filter_by(username='bhumika').first()
    role = Role.query.filter_by(name='creator').first()

    if user and role:
        user.roles.append(role)
        db.session.commit()