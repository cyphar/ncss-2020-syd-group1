import datetime
#get current time (anyone can use this to get local time)
#Don't DELETE!!!
#--------------------------------------------------------
def get_time():
  now = datetime.now()
  hour = int(now.strftime("%H")) + 11
  current_time = now.strftime(f"{hour}%M")
  print(current_time)
  return current_time
def get_date():
  now = datetime.now()
  current_date = now.strftime(f"%Y%m%d")
  print(current_date)
  return current_date
#--------------------------------------------------------
