"""this file was made for the class that will represent the
database used to store users and their ratings"""
# pylint: disable=E1101
# pylint: disable=C0413
# pylint: disable=W0603
# pylint: disable=W0611
# pylint: disable=W1508
# pylint: disable=R0903
import flask_sqlalchemy
from app import DB


class allusers(DB.Model):
    """this is the class used to objectify the database in python
    i tried changing the name to pascal case but was thrown errors
    that had to do with the db, which is too deep for me to touch
    with this little time left on this project"""
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(), unique=True)
    rating = DB.Column(DB.Integer)

    def __init__(self, name, rate):
        self.username = name
        self.rating = rate
