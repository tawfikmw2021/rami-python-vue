from flask_login import UserMixin

from project import utils
from . import db
from sqlalchemy import ARRAY, Integer, Column

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    np = db.Column(db.Integer)
    players = db.Column(db.String(1000))
    rounds = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    time = db.Column(db.String(1000))


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    game_id = db.Column(db.Integer)
    np = db.Column(db.Integer)
    players = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    state = db.Column(db.String(1000))
    time = db.Column(db.String(1000))
