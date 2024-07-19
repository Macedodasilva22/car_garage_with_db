# models/car.py
from app import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(150), nullable=False)
    problems = db.relationship('Problem', backref='car', lazy=True)
