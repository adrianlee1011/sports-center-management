from flask_wtf import Form, FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from wtforms.fields.html5 import DateField

class RegisterForm(Form):
  name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sing Up')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email already registered.')


class LoginForm(Form):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember me')
  submit = SubmitField('Login')

class UpdateAccountForm(Form):
  email = StringField('Email', validators=[DataRequired(), Email()])
  card_number = StringField('Card')
  card_expiry = StringField('Expiry')
  card_CVC = StringField('CVC')
  submit = SubmitField('Update')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('Email already registered.')

class BookingForm(Form):
  date_time = DateField('Date', validators=[DataRequired()])
  time = SelectField('Time', coerce=int, choices=([1, "08:00"], [2, "09:00"], [3, "10:00"], [4, "11:00"], [5, "12:00"], [6, "13:00"], [7, "14:00"], [8, "15:00"], [9, "16:00"]))
  activity = SelectField('Activity', coerce=int, choices=[])
  duration = SelectField('Duration', coerce=int, choices=([1, 1], [2, 2]))
  payment = SelectField('Payment method', coerce=int, choices=([1, "Cash"], [2, "Card"]))
  submit = SubmitField('Make Booking')

class ChangeTimetable(FlaskForm):
  date = DateField('Date')
  submit = SubmitField('Change Date')

class ManageFacilities(Form):
  swimming_pool = TextAreaField('Swimming Pool')
  fitness_room = TextAreaField('Fitness Room')
  squash_court = TextAreaField('Squash Courts')
  sports_hall = TextAreaField('Sports Hall')
  submit = SubmitField('Save Changes')