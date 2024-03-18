from src import db
from src.api.users.models import User


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def add_user(fname, lname, username):
    user = User(fname= fname, lname= lname, username=username)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, fname=None, lname=None, username=None):
    if fname is not None:
        user.fname = fname
    if lname is not None:
        user.lname = lname
    if username is not None:
        user.username = username

    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user