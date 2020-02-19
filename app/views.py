from flask import render_template, flash, url_for, redirect, request, abort
from app import app, db, models, bcrypt
from flask_sqlalchemy import SQLAlchemy
from .forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
  page = request.args.get('page', 1, type=int)
  posts = models.Post.query.order_by(models.Post.date.desc()).paginate(page=page, per_page=4)
  return render_template('home.html', posts=posts)

@app.route('/about')
def about():
  return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegisterForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = models.User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
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
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Account has been updated', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  return render_template('account.html', title="Account", form=form)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
  post = models.Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Post deleted!', 'success')
  return redirect(url_for('home'))

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