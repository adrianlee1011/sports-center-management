from app import db, models
from datetime import datetime, date, time
import random

def get_week_number(date):
  var = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
  return datetime.strftime(var, '%W')

def clear_data(session):
  meta = db.metadata
  for table in reversed(meta.sorted_tables):
    session.execute(table.delete())
  session.commit()

def make_url(name):
  url = name.replace(" ", "_")
  return url.lower()

clear_data(db.session)

# Adding into Facility table
f_name = ["Swimming Pool", "Fitness Room", "Squash Court 1", "Squash Court 2", "Squash Court 3", "Squash Court 4", "Sports Hall"]
f_capacity = [32, 25, 4, 4, 4, 4, 20]

for i in range(7):
  f = models.Facility(id=i+1, name=f_name[i], capacity=f_capacity[i], url=make_url(f_name[i]))
  db.session.add(f)
  db.session.commit()

# Adding into Activity table
a_activity = [[1, "Swimming Lesson"], [1, "Water Polo"], [1, "Scuba Diving"], [1, "Triathlon"], [2, "Zumba lesson"], [2, "HIIT Challenge"], [2, "Cardio Evolution"],[2, "Pilates"], [2, "Circuit Challenge"], [3, "Squash Training"], [3, "Junior Squash Training"], [3, "Private Session"], [7, "Basketball"], [7, "Badminton"], [7, "Netball"], [7, "Futsall"], [7, "Volleyball"]]



for i in range(len(a_activity)):
  a = models.Activity(id=i+1, facility=a_activity[i][0], name=a_activity[i][1], url=make_url(a_activity[i][1]))
  db.session.add(a)
  db.session.commit()

# Adding into Booking table
limit = 100 # bookings generated for each facility

for i in range(len(f_name)):
  current_day = 10 # day of the month
  current_time = 8 # start time
  current_month = 3 # start month
  activity_index = []
 
  # squash courts have same activities
  if i > 1 and i < 6:
    for index in range(len(a_activity)):
      if a_activity[index][0] == 3:
        activity_index.append(index)
  else:
    for index in range(len(a_activity)):
      if a_activity[index][0] == i + 1:
        activity_index.append(index)

  if i > 1:
    activity_index.append(-1)
 
  for j in range(limit):
    user = random.randint(1, 200)
    duration = 1
    if j % 5 == 0:
      duration = 2
    activity_type = random.choice(activity_index)
    paid = random.randint(0, 1)
    if current_time + duration > 17:
      current_day += 1
      current_time = 9 + random.randint(0, 3)
    if current_day > 30:
      current_day = 1
      current_month += 1
 
    time_string = str(current_time)
    date_time = f"2020-{current_month}-{current_day} {time_string.zfill(2)}:00:00"

    b = models.Booking(id=limit*i+j+1, facility=i+1, user=user, datetime=datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'), week=int(get_week_number(str(date_time))), year=2020, duration=duration, activity=activity_type, paid=paid)
    db.session.add(b)
    db.session.commit()
 
    current_time += duration + random.randint(0, 5)

