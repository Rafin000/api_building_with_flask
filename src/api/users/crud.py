from src import db
from src.api.users.transformers import transform_user
from src.api.users.models import User
from werkzeug.security import generate_password_hash

def get_all_users():
    return [transform_user(user) for user in User.query.all()]


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def add_user(fname, lname, username, password):
    user = User(fname= fname, lname= lname, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    db.session.close()
    return user


def update_user(user, fname=None, lname=None, username=None, password=None):
    if fname is not None:
        user.fname = fname
    if lname is not None:
        user.lname = lname
    if username is not None:
        user.username = username
    if password is not None:
        user.password = generate_password_hash(password)

    db.session.commit()
    db.session.close()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return user


