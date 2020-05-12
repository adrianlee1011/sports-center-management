from app import db, models, bcrypt
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
f_description = ["""Pricing: £2 per session\n
        There is a discount for booking multiple sessions in advance\n
        Capacity: 25\n
        Our newly refurbished fitness room contains a range of equipment including free weights, treadmills and rowing machines. It can only be booked for General Use""", """Pricing: £2 per session
        <h5>There is a discount for booking multiple sessions in advance</h5>
        <h4>Capacity: 20</h4>
        <h4><br>Our large Sports Hall can be used to play a variety of games and can be booked for 1-hour sessions</h4>""", """<h4>Pricing: £5 per session</h4>
        <h5>There is a discount for booking multiple sessions in advance</h5>
        <h4>Capacity: 4</h4>
        <h4><br>This is one of our four squash courts that can be booked for 1-hour sessions as well as team events</h4>""", """<h4>Pricing: £5 per session</h4>
        <h5>There is a discount for booking multiple sessions in advance</h5>
        <h4>Capacity: 4</h4>
        <h4><br>This is one of our four squash courts that can be booked for 1-hour sessions as well as team events</h4>""", """<h4>Pricing: £5 per session</h4>
        <h5>There is a discount for booking multiple sessions in advance</h5>
        <h4>Capacity: 4</h4>
        <h4><br>This is one of our four squash courts that can be booked for 1-hour sessions as well as team events</h4>""", """<h4>Pricing: £5 per session</h4>
        <h5>There is a discount for booking multiple sessions in advance</h5>
        <h4>Capacity: 4</h4>
        <h4><br>This is one of our four squash courts that can be booked for 1-hour sessions as well as team events</h4>""", """<h4>Pricing: £2 per session</h4>
        <h5>There is a discount for booking multiple sessions in advance</h5>
        <h4>Capacity: 32</h4>
        <h4><br>This is a stae of the art swimming pool with multiple lanes for different speed swimmers. It can be booked for General Use, Lane Swimming, Lessons, or Team Events</h4>"""]

for i in range(7):
  f = models.Facility(id=i+1, name=f_name[i], capacity=f_capacity[i], url=make_url(f_name[i]), description=f_description[i])
  db.session.add(f)
  db.session.commit()

print("Facility table generated!")

# Adding into Activity table
a_activity = [[1, "Swimming Lesson"], [1, "Water Polo"], [1, "Scuba Diving"], [1, "Triathlon"], [2, "Zumba lesson"], [2, "HIIT Challenge"], [2, "Cardio Evolution"],[2, "Pilates"], [2, "Circuit Challenge"], [3, "Squash Training"], [3, "Junior Squash Training"], [3, "Private Session"], [7, "Basketball"], [7, "Badminton"], [7, "Netball"], [7, "Futsall"], [7, "Volleyball"]]



for i in range(len(a_activity)):
  a = models.Activity(id=i+1, facility=a_activity[i][0], name=a_activity[i][1], url=make_url(a_activity[i][1]))
  db.session.add(a)
  db.session.commit()

print("Activity table generated!")

# Adding into Booking table
limit = 200 # bookings generated for each facility

for i in range(len(f_name)):
  current_day = 10 # day of the month
  current_time = 8 # start time
  current_month = 5 # start month
  activity_index = []

  print("Booking table (" + str(int(i)) + "/7)")
 
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
    user = random.randint(2, 201)
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

    b = models.Booking(id=limit*i+j+1, facility=i+1, user=user, datetime=datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'), week=int(get_week_number(str(date_time))), year=2020, duration=duration, activity=activity_type+1, paid=paid)
    db.session.add(b)
    db.session.commit()
 
    current_time += duration + random.randint(0, 5)

print("Booking table generated!")

# Adding into User table
u = models.User(id=1, name="Manager", email="Sports.Centre.Manager@gmail.com", password=bcrypt.generate_password_hash("secret_password").decode('utf-8'), user_type=3, card_number="none", card_expiry="none", card_CVC="none")

u_names = ["Jacquetta Brakefield", "Genaro Jakubowski", "Amparo Bernal", "Karlyn Basch", "Tisha Cordon", "Voncile Weekes", "Krystin Felten", "Gertha Kitchin", "Vernie Mika", "Charley Merkle", "Fannie Murtagh", "Chantel Fontenot", "Chandra Fabela", "Gearldine Lansing", "Hillary Rahman", "Jacki Delahoussaye", "Shauna Dewey", "Elias Turley", "Jona Shane", "Thao Goudy", "Lottie Ducker", "Kina Corona", "Hanna Correa", "Rikki Bolten", "Rod Penepent", "Tiny Haider", "Jared Kumm", "Willette Fulton", "Rhett Mcgraw", "Mariam Liebig", "Annis Mailman", "Gerard Davies", "Paul Summitt", "Darci Orton", "Andra Wycoff", "Carmelo Schick", "Joselyn Slane", "Johna Gerardi", "Daphine Lundblad", "Mellisa Harjo", "Yadira Bryant", "Jonnie Spainhour", "Otilia Dishman", "Suellen Eberhard", "Augustina Newberg", "Lauralee Tunnell", "Elsy Chowdhury", "Novella Gough", "Queen Lafave", "Denise Marse", "Edyth Monson", "Caryn Sorber", "Malinda Clanton", "Patrick Corbitt", "Kimi Gilland", "Sharron Wikoff", "Eddy Trotman", "Gregory Gerdes", "Awilda Ledoux", "Tamela Kyer", "Ali Licata", "Tasha Mchone", "Ellie Bassett", "Geralyn Longmire", "Galina Flynn", "Cheree Schaar", "Santana Faddis", "Sarita Siders", "Georgene Lamark", "Madaline Rossi", "Shanon Conant", "Merry Golliday", "Myrl Brannon", "Hester Dupuy", "Neoma Mcdougle", "Dominic Groen", "Willette Jose", "April Jackman", "Fran Hess", "Angella Duffel", "Vera Macomber", "Tia Mickley", "Valarie Gula", "Lyndon Bizier", "Majorie Maskell", "Silva Hickey", "Clarita Pille", "Cris Fennessey", "Joann Tremblay", "Tana Broaddus", "Kara Niebuhr", "Maragaret Jardin", "Dario Sturgis", "Emery Counts", "Chloe Turley", "Carlos Way", "Carl Linhart", "Micha Hollowell", "Patria Adamson", "Berniece Guillermo", "Patrica Peller", "Andrea Lykes", "Nanci Daffron", "Marline Corkill", "Karol Deak", "Regena Villicana", "Brynn Byrge", "Florentino Ohman", "Arnetta Rusin", "Lael Eslick", "Pandora Holt", "Bradford Bivona", "Margarett Vergara", "Maudie Padro", "Sharika Kinch", "Harriette Bye", "Marg Goddard", "Lenny Hupp", "Lakeesha Omeara", "Tony Montenegro", "Gilberte Viveiros", "Freida Akers", "Palmira Metz", "Francesca Ruhl", "Thelma Dolloff", "Leda Knapik", "Meridith Linder", "Cassy Strawbridge", "Shawn Doxey", "Dayna Miyamoto", "Aleen Ratley", "Angelia Lindner", "Jewell Morse", "Carlie Reis", "Marielle Points", "Tamala Pounders", "Camie Brickhouse", "Keesha Poteat", "Jayne Dakin", "Shera Wink", "Hollis Wendler", "Babara Caines", "Kathryn Ybanez", "Tequila Nathan", "Chase Shadduck", "Vicenta Kindig", "Delbert Meneses", "Rocky Guess", "Nella Flakes", "Danial Nicolosi", "Kurt Pai", "Wesley Mullenax", "Coleman Brazeal", "Doris Ledgerwood", "Donnie Hornstein", "Ardath Redrick", "Irving Badillo", "Felix Braley", "Stacy Parchman", "Larae Kayser", "Yajaira Bisceglia", "Rolland Stauffer", "Karey Kawakami", "Jamison Velasquez", "Marcel Cichon", "Johna Leister", "Tamie Reeves", "Sue Chenard", "Trinh Patel", "Minnie Narcisse", "Kenia Bolt", "Hortencia Laurent", "Nelly Corman", "Wilbert Vanbuskirk", "Junior Mclemore", "Akilah Nolin", "Francisco Voisine", "Bev Thiry", "Bea Nevius", "Andera Hilty", "Audrie Salls", "Rubie Tito", "Buena Magby", "Brendon Trieu", "Roselia Port", "Kathaleen Lobato", "Nathanael Boggan", "Talitha Morriss", "Robert Causby", "Kam Tiggs", "Nichol Henery", "Lacresha Bissette", "Shanice Nath", "Jaquelyn Mcchesney", "Inocencia Erlandson", "Hanna Surratt", "Ricki Redmond", "Guy Hakim", "Elias Hoban", "Daniella Bonar"]

for i in range(len(u_names)):
  names = u_names[i].split()
  u_email = names[0] + '.' + names[1] + "@gmail.com"
  u_password = bcrypt.generate_password_hash("secret_password").decode('utf-8')
  u = models.User(id=i+2, name=u_names[i], email=u_email, password=u_password, user_type=1, card_number="none", card_expiry="none", card_CVC="none")
  db.session.add(u)
  db.session.commit()
  if i%20 == 0:
    print("User table (" + str(int(i/20)) + "/10)")

print("User table generated!")

print("Database successfully generated!")