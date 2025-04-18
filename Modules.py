from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Main import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
        return f'<User {self.username}>'