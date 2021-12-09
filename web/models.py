from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Boolean, String, DateTime, Integer, Numeric, ForeignKey, Text
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

# the original database specification for keeping track of the tasks
# ORM mapping
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    reset_token = db.Column(db.String(1000))

    todos = db.relationship('Todo', backref="creator", lazy=True)
    # timers = db.relationship('Timer', backref="creator", lazy=True)


    def __repr__(self):
        return "<User(id={}, username={}, email={}".format(self.id, self.username, self.email)
 
class Timer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    focus = db.Column(db.Integer, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

class Todo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    do = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
