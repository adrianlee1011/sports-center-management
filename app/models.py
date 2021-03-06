from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  user_type = db.Column(db.Integer, default=1)
  card_number = db.Column(db.String, default="none")
  card_expiry = db.Column(db.String, default="none")
  card_CVC = db.Column(db.String, default="none")

class Facility(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  capacity = db.Column(db.Integer)
  url = db.Column(db.String(100))
  description = db.Column(db.String, default="No description available!")

class Booking(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  facility = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.Column(db.Integer, db.ForeignKey('facility.id') , nullable=False)
  datetime = db.Column(db.DateTime, nullable=False)
  week = db.Column(db.Integer)
  year = db.Column(db.Integer)
  duration = db.Column(db.Integer, nullable=False)
  activity = db.Column(db.Integer, nullable=False)
  paid = db.Column(db.Integer, default=0)

class Activity(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  facility = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
  name = db.Column(db.String)
  url = db.Column(db.String(100))