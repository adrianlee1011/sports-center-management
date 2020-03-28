from datetime import datetime
from datetime import timedelta

def get_dates_for_week(year, week):
  date = datetime.strptime(str(year), "%Y")
  date += timedelta(weeks=week)
  dates = []
  for i in range(7):
    dates.append(datetime.strftime(date + timedelta(days=i), '%d/%m'))
  return dates




week = 10
year = 2020

date = datetime.strptime("2020", '%Y')
now = datetime.now()

print(date)
print(now + timedelta(weeks=1))

print(get_dates_for_week(2020, 10))