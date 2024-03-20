from src import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(128), nullable=False)
    lname = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_date = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    jobs = db.relationship('Job', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, fname, lname, username, password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)