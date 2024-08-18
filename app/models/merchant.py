# models/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Password should be hashed