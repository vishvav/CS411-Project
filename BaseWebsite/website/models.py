# this file contains the models for the database
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Picture(db.Model):  # type: ignore
    # each picture can have a name, a description, date, and corresponding user
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):  # type: ignore
    # each user can have a name, email, password, and corresponding picture list
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    # one user can have many pictures
    pictures = db.relationship('Picture')
