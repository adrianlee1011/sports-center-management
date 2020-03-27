from flask import render_template, flash, url_for, redirect, request, abort
from app import app, db, models, bcrypt
from flask_sqlalchemy import SQLAlchemy
from .forms import RegisterForm, LoginForm, UpdateAccountForm, BookingForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


def get_week_number(date):
  week = datetime.strftime(date, "%W")
  return week

def get_year_number(date):
  year = datetime.strftime(date, "%Y")
  return year

def get_current_week():
  current = int(datetime.strftime(datetime.now(), "%W"))
  return current

def get_current_year():
  current = int(datetime.strftime(datetime.now(), "%Y"))
  return current

def filter_by_week(bookings):
  new = []
  for query in bookings:
    if get_week_number(query.datetime) == get_current_week():
      new.append(query)
  return new

def is_integer_sequence(sequence, length):
  if sequence == "none":
    return True
  if len(sequence) != length:
    return False
  if sequence.isdigit():
    return True
  return False

def is_booking_available(facility, date_time, duration):
  # check bookings for the same hour
  same_hour = models.Booking.query.filter_by(facility=facility).filter_by(datetime=datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')).count()
  if same_hour != 0:
    return False
  # check bookings for the closing time
  if int(date_time[11:13]) + duration > 17:
    return False
  # check booking starting an hour earlier (because it could have duration 2 hours)
  if int(date_time[11:13]) - 1 < 10:
    prev_date = date_time[:11] + '0' + str(int(date_time[11:13]) - 1) + date_time[13:]
  else:
    prev_date = date_time[:11] + str(int(date_time[11:13]) - 1) + date_time[13:]
  prev_hour = models.Booking.query.filter_by(facility=facility).filter_by(datetime=datetime.strptime(prev_date, '%Y-%m-%d %H:%M:%S')).filter_by(duration=2).count()
  if prev_hour != 0:
    return False
  # check booking starting an hour later (because the booking could have duration 2 horus)
  if int(date_time[11:13]) + 1 < 10:
    next_date = date_time[:11] + '0' + str(int(date_time[11:13]) + 1) + date_time[13:]
  else:
    next_date = date_time[:11] + str(int(date_time[11:13]) + 1) + date_time[13:]
  next_hour = models.Booking.query.filter_by(facility=facility).filter_by(datetime=datetime.strptime(next_date, '%Y-%m-%d %H:%M:%S')).count()
  if next_hour != 0 and duration == 2:
    return False
  return True

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
    flash("Account created for %s!" %form.name.data, 'success')
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
    if is_integer_sequence(form.card_number.data, 16) and is_integer_sequence(form.card_expiry.data, 4) and is_integer_sequence(form.card_CVC.data, 3):
      current_user.card_number = form.card_number.data
      current_user.card_expiry = form.card_expiry.data
      current_user.card_CVC = form.card_CVC.data
      db.session.commit()
      flash('Account has been updated', 'success')
    else:
      flash('Invalid card details', 'danger')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.email.data = current_user.email
    form.card_number.data = current_user.card_number
    form.card_expiry.data = current_user.card_expiry
    form.card_CVC.data = current_user.card_CVC
  return render_template('account.html', title="Account", form=form)

@app.route('/my_bookings', methods=['GET', 'POST'])
@login_required
def my_bookings():
  # view bookings
  bookings = models.Booking.query.order_by(models.Booking.id.asc()).filter_by(user=current_user.id)
  facilities = models.Facility.query.order_by(models.Facility.id.asc())
  activities = models.Activity.query.order_by(models.Activity.id.asc())

  # make a booking
  form = BookingForm()
  form.activity.choices = [(activity.id, activity.name) for activity in models.Activity.query.all()]
  if form.validate_on_submit():
    act = models.Activity.query.filter_by(id=form.activity.data).first()
    facility_id = act.facility
    if is_booking_available(facility_id, form.date_time.data, form.duration.data):
      booking = models.Booking(facility=facility_id, user=current_user.id, datetime=datetime.strptime(form.date_time.data, '%Y-%m-%d %H:%M:%S'), week=get_week_number(datetime.strptime(form.date_time.data, '%Y-%m-%d %H:%M:%S')), year=get_year_number(datetime.strptime(form.date_time.data, '%Y-%m-%d %H:%M:%S')), duration=form.duration.data, activity=form.activity.data)
      db.session.add(booking)
      db.session.commit()
      flash("Success! Booking made!", "success")
    else:
      flash("Booking not available for the chosen time.", "danger")
    return redirect(url_for('my_bookings'))
  return render_template('my_bookings.html', title="My Bookings", bookings=bookings, facilities=facilities, activities=activities, form=form)

@app.route('/facilities')
def facilities():
  year = get_current_year()
  week = get_current_week()
  facilities = models.Facility.query.order_by(models.Facility.id.asc())
  return render_template('facilities.html', title="Facilities", facilities=facilities, year=year, week=week)

@app.route('/facilities/<facility_url>/<int:year>/<int:week>')
def show_facility(facility_url, year, week):
  facility = models.Facility.query.filter_by(url=facility_url).first_or_404()

  bookings = []
  for i in range(8):
    b = models.Booking.query.filter_by(facility=facility.id).filter_by(week=week).filter_by(year=year)
    filtered_b = []
    for query in b:
      if query.datetime.weekday() == i-1:
        filtered_b.append(query)
    bookings.append(filtered_b)
  
  address = 'facilities/' + facility.url + '.html'
  title = facility.name

  activity = models.Activity.query.order_by(models.Activity.id.asc())
  return render_template(address, title=title, bookings=bookings, url='/facilities/'+facility_url, year=year, week=week, activity=activity)

@app.route('/activities')
def activities():
  year = get_current_year()
  week = get_current_week()
  url = '/activities/' + str(year) + '/' + str(week)
  return redirect(url)

@app.route('/activities/<int:year>/<int:week>')
def activities_timetable(year, week):
  bookings = []
  for i in range(8):
    b = models.Booking.query.order_by(models.Booking.id.asc()).filter_by(week=week).filter_by(year=year)
    filtered_b = []
    for query in b:
      if query.datetime.weekday() == i-1 and query.activity != -1:
        filtered_b.append(query)
    bookings.append(filtered_b)
  
  activity = models.Activity.query.order_by(models.Activity.id.asc())
  return render_template('activities.html', title='Activities', bookings=bookings, year=year, week=week, activity=activity, url='/activities')

@app.route('/activities/<activity_url>/<int:year>/<int:week>')
def show_activity(activity_url, year, week):
  activity = models.Activity.query.filter_by(url=activity_url).first_or_404()

  bookings = []
  for i in range(8):
    b = models.Booking.query.order_by(models.Booking.id.asc()).filter_by(activity=activity.id).filter_by(week=week).filter_by(year=year)
    filtered_b = []
    for query in b:
      if query.datetime.weekday() == i-1:
        filtered_b.append(query)
    bookings.append(filtered_b)
  
  address = 'activities_index.html'
  title = activity.name

  activity = models.Activity.query.order_by(models.Activity.id.asc())
  return render_template(address, title=title, bookings=bookings, year=year, week=week, activity=activity, url='/activities/'+activity_url)

@app.errorhandler(403)
def access_forbidden_error(error):
  return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('errors/500.html'), 500