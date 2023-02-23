from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    directory = db.Column(db.String(255))
    command = db.Column(db.Text)
    last_run = db.Column(db.DateTime)

