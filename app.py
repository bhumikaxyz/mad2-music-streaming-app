from musicapp import app, db
from flask import render_template
from musicapp.models import User, Role
# from musicapp.sec import datastore
# from flask_security.utils import get_random_token


with app.app_context():
    db.create_all()

    # user = User.query.filter_by(username='bhumika').first()
    # role = Role.query.filter_by(name='admin').first()

    # if user and role:
    #     user.roles.append(role)
    #     db.session.commit()

    # if not app.security.datastore.find_user(username='user1'):
    #     app.security.datastore.create_user(name='user1', username='user1', password_hash='user1')

    # admin_role = datastore.find_or_create_role(name="admin", description="User is an Admin")
    # creator_role = datastore.find_or_create_role(name="creator", description="User is a Creator")
    # user_role = datastore.find_or_create_role(name="user", description="User is a User")
    
    # # Commit to save roles
    # db.session.commit()

    # # Function to create user if not exists
    # def create_user_if_not_exists(name, email, username, password_hash, *roles):
    #     if not datastore.find_user(email=email):
    #         datastore.create_user(
    #             name=name,
    #             username=username,
    #             email=email,
    #             password_hash=password_hash,
    #             roles=list(roles),
    #             active=True
    #         )
    
    # # Create users
    # create_user_if_not_exists('user1', "admin@email.com","sri1","1", admin_role)
    # # create_user_if_not_exists("creator1@email.com","sri2", "1", creator_role)
    # # create_user_if_not_exists("stud1@email.com","sri3", "1", user_role)
    # # create_user_if_not_exists("stud2@email.com", "sri4","1", user_role)

    # # Commit to save users
    # db.session.commit()


   
if __name__ == '__main__':
    app.run(debug = True) 



