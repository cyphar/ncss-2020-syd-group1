import vobject, requests

def public_holiday(input_date):
  holiday = requests.get('https://www.vic.gov.au/sites/default/files/2019-11/Victorian_public_holiday_dates.ics')
  print(holiday.text)
  cal = vobject.readOne(holiday.text)

  for item in cal.vevent_list:
    if item.dtstart.value == input_date.date():
      return item.summary.value
  return False
