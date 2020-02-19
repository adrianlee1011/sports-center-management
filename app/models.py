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
  password_hash = db.Column(db.String(50), nullable=False)
  user_type = db.Column(db.Integer, nullable=False)
  card_number = db.Column(db.Integer, default=0)
  card_expiry = db.Column(db.Integer, default=0)
  card_CVC = db.Column(db.Integer, default=0)

class Facility(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  capacity = db.Column(db.Integer)

class Booking(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  facility = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.Column(db.Integer, db.ForeignKey('facility.id') , nullable=False)
  datetime = db.Column(db.DateTime, nullable=False)
  duration = db.Column(db.Integer, nullable=False)