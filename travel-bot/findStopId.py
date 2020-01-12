import requests
#this function will return stop ids for the given locations from the user.
#it will be called within the trip planner function in order to retrieve id parameters for the api.
# example stop finder request
#findStopId({location address})
def findStopId(location):


  stops = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/stop_finder?outputFormat=rapidJSON&name_sf={location}&coordOutputFormat=EPSG:4326&TfNSWSF=true&version=10.2.1.42&type_sf=stop', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})

  stops = stops.json()

  stops = stops['locations']

  stopQuality = 0
  stopId = 0


  for stop in stops:
    if stop['matchQuality'] > stopQuality:
      stopQuality = stop['matchQuality']
      stopId = stop['id']
      # print(stopID)
  return stopId
