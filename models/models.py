from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    directory = db.Column(db.String(255), nullable=False)
    command = db.Column(db.Text, nullable=False)
    token = db.Column(db.String(40), nullable=False)
    last_run = db.Column(db.DateTime)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
