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
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    reset_token = db.Column(db.String(1000))
    block = db.Column(db.Boolean, default=True)
    
    tasks = db.relationship('Tasks', backref="creator", lazy=True)
    timers = db.relationship('Timer', backref="creator", lazy=True)

    def __repr__(self):
        return "<User(id={}, username={}, email={}".format(self.id, self.username, self.email)
 
 # timer table
class Timer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    focus_time = db.Column(db.Integer, nullable=False)
    attempted_time = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
# tasks table 
class Tasks(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    doing = db.Column(db.Boolean, default=True)
    time_created = db.Column(db.DateTime, nullable=False)
    time_completed = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
