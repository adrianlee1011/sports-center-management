from flask import render_template, flash, url_for, redirect, request, abort
from app import app, db, models, bcrypt
from flask_sqlalchemy import SQLAlchemy
from .forms import RegisterForm, LoginForm, UpdateAccountForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html', title='About')

@app.route('/index')
def index():
  return render_template('index.html', title='Index')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegisterForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = models.User(name=form.name.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.name.data}!', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = models.User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      if next_page:
        return redirect(next_page)
      else:
        return redirect(url_for('home'))
    else:
      flash('Invalid details', 'danger')
  return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    current_user.email = form.email.data
    current_user.card_number = form.card_number.data
    current_user.card_expiry = form.card_expiry.data
    current_user.card_CVC = form.card_CVC.data
    db.session.commit()
    flash('Account has been updated', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.email.data = current_user.email
  return render_template('account.html', title="Account", form=form)

@app.errorhandler(403)
def access_forbidden_error(error):
  return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('/errors/500.html'), 500