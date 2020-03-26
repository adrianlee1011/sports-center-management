from app import db, models
from datetime import datetime, date, time

def get_week_number(date):
  var = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
  return datetime.strftime(var, '%W')

def clear_data(session):
  meta = db.metadata
  for table in reversed(meta.sorted_tables):
    session.execute(table.delete())
  session.commit()

clear_data(db.session)

# Adding into Facility table
f_name = ["Swimming Pool", "Fitness Room", "Squash Court 1", "Squash Court 2", "Squash Court 3", "Squash Court 4", "Sports Hall"]
f_capacity = [32, 25, 4, 4, 4, 4, 20]
f_url = ["swimming_pool", "fitness_room", "squash_court_1", "squash_court_2", "squash_court_3", "squash_court_4", "sports_hall"]

for i in range(7):
  f = models.Facility(id=i+1, name=f_name[i], capacity=f_capacity[i], url=f_url[i])
  db.session.add(f)
  db.session.commit()

# Adding into Booking table
b_facility = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2]
b_user = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 1, 2, 3, 1, 2, 1, 3, 4, 1, 2, 3, 4, 2]
b_datetime = ["2020-03-12 15:00:00", "2020-3-10 14:00:00", "2020-03-10 13:00:00", "2020-03-15 15:00:00", "2020-03-19 10:00:00", "2020-03-14 09:00:00", "2020-03-13 12:00:00", "2020-03-12 16:00:00", "2020-03-11 11:00:00", "2020-03-12 10:00:00", "2020-03-19 12:00:00", "2020-03-12 17:00:00", "2020-03-11 09:00:00", "2020-03-18 13:00:00", "2020-03-13 12:00:00", "2020-03-14 16:00:00", "2020-03-13 11:00:00", "2020-03-15 13:00:00", "2020-03-16 15:00:00", "2020-03-15 10:00:00", "2020-03-16 14:00:00", "2020-03-15 14:00:00", "2020-03-16 15:00:00", "2020-03-17 15:00:00", ]
b_duration = [1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
b_activity = [-1, 0, 1, 2, -1, 0, 1, 2, -1, 0, 1, 2, -1, 0, 1, 2, -1, 0, 1, 2, -1, 0, 1, 2, -1, 0, 1, 2]
b_paid = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 , 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]

for i in range(24):
  b = models.Booking(id=i+1, facility=b_facility[i], user=b_user[i], datetime=datetime.strptime(b_datetime[i], '%Y-%m-%d %H:%M:%S'), week=int(get_week_number(b_datetime[i])), year=2020, duration=b_duration[i], activity=b_activity[i], paid=b_paid[i])
  db.session.add(b)
  db.session.commit()

# Adding into Activity table
a_activity = [[1, "Swimming Lesson"], [1, "Water Polo"], [1, "Scuba Diving"], [1, "Triathlon"], [2, "Zumba lesson"], [2, "HIIT Challenge"], [2, "Cardio Evolution"],[2, "Pilates"], [2, "Circuit Challenge"], [3, "Squash Training"], [3, "Junior Squash Training"], [3, "Private Session"], [4, "Squash Training"],[4, "Junior Squash Training"], [4, "Private Session"], [5, "Squash Training"], [5, "Junior Squash Training"], [5, "Private Session"], [6, "Squash Training"],[6, "Junior Squash Training"], [6, "Private Session"], [7, "Basketball"], [7, "Badminton"], [7, "Netball"], [7, "Futsall"], [7, "Volleyball"]]

for i in range(len(a_activity)):
  a = models.Activity(id=i+1, facility=a_activity[i][0], name=a_activity[i][1])
  db.session.add(a)
  db.session.commit()