import flask_sqlalchemy
from app import db

class allusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    rating = db.Column(db.Integer)
    
    def __init__(self, a, b):
        self.username = a
        self.rating = b