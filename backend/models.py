from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    password = db.Column(db.String(10), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(50))
