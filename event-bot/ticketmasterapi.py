import requests
from datetime import datetime, timedelta
import time
def ticketmaster(postCode = 2000,page = 0):
  tommorows_tommorow = (datetime.now() + timedelta(days = 2)).strftime('%Y-%m-%dT%H:%M:%SZ')
  events = []
  response = requests.get(f'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=AU&apikey=2mjfi7kJqsuGwrSFAVy0ehhzriG9F3ds&postalCode={postCode}&page={page}&endDateTime={tommorows_tommorow}')
  text = response.json()
  for index in range(len(text['_embedded']['events'])):
      is_repeat = False
      name = text['_embedded']['events'][index]['name']
      venue = text['_embedded']['events'][index]['_embedded']['venues'][0]['name']
      local_time = text['_embedded']['events'][index]['dates']['start']['localTime']
      classification = text['_embedded']['events'][index]['classifications'][0]['segment']['name']
      startDT = datetime.strptime(text['_embedded']['events'][index]['dates']['start']['dateTime'],'%Y-%m-%dT%H:%M:%SZ')
      endDT = startDT + timedelta(hours=3)
      address = text['_embedded']['events'][index]['_embedded']['venues'][0]['address']['line1']
      lon = text['_embedded']['events'][index]['_embedded']['venues'][0]['location']['longitude']
      lat = text['_embedded']['events'][index]['_embedded']['venues'][0]['location']['latitude' ]
      for jindex in range(len(events)):
          if name in events[jindex]['name'] or 'not for sale' in name:
              is_repeat = True
      if is_repeat == False:
          event = {
              'name':name,
              'place':venue,
              'time':local_time,
              'type':classification,
              'api':True,
              'current_topic':{
                  'relevant_location':{
                      'address':address,
                      'lat':lat,
                      'long':lon,
                  },
                  'start_time': time.mktime(startDT.timetuple()),
                  'end_time': time.mktime(endDT.timetuple()),
              }}

          events.append(event)
  return events


