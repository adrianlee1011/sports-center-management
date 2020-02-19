from flask_wtf import Form
from flask_login import current_user
from wtforms import StringField, DateField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

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
  card_number = IntegerField('Card')
  card_expiry = IntegerField('Expiry')
  card_CVC = IntegerField('CVC')
  submit = SubmitField('Update')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('Email already registered.')