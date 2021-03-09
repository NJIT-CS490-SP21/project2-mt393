import flask_sqlalchemy
from app import db

class allusers(db.Model):
    username = db.Column(db.String(), primary_key=True)
    rating = db.Column(db.Integer)
    
    def __init__(self, a, b):
        self.username = a
        self.rating = b