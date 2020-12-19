#
#  Taken from the tutorial at: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
#
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))