from click import DateTime
from sqlalchemy import Date
from src import db


class Job(db.Model):

    __tablename__= 'jobs'

    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    company = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date)

    def __init__(self, title, company, user_id, start_date, end_date=None):
        self.title = title
        self.company = company
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
     