import requests
import findStopId
import json

def planTrip(date, time, start, end, get_value):
  trips = None
  if get_value == "here":
    trips = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&itdDate=20200114&itdTime=1200&type_origin=coord&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42&depArrMacro=arr', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})
  elif get_value == "manual":
    trips = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&depArrMacro=dep&itdDate=20200114&itdTime=1200&type_origin=any&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})

  #https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&depArrMacro=dep&itdDate={date}&itdTime={time}&type_origin=coord&name_origin={start}&depArrMacro=arr&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42
  get_json = trips.json()
  # journeys = get_json["journeys"]
  # print(journeys)
  # system_messages = get_json["systemMessages"]
  print(get_json)

  for journey in get_json["journeys"]:
    legs = journey["legs"]
    fares = journey["fare"]

    #duartion measured in seconds
    totalDuration = 0

    summary = []

    route_types = {
      1: "Train",
      4: "Light Rail",
      5: "Bus",
      7: "Coach",
      9: "Ferry",
      11: "School Bus",
      99: "Walk",
      100: "Walk"
    }

    route_type = None
    travel_steps = []

    legNumber = 0
    for leg in legs:
      totalDuration += leg["duration"]
      #print(f"totalDuration: {totalDuration}")
      origin = leg["origin"]
      destination = leg["destination"]
      # print(f"destination: {destination}")
      # if legNumber == 0:
      #   depart =
      route_type = leg['transportation']['product']['class']
      #print(f"route_type: {route_type}")
      transport_method = route_types[route_type]
      duration_minutes = int(leg["duration"] / 60)
      travel_steps.append((transport_method, duration_minutes))
      #print("\n")
    #print(f"travel_steps: {travel_steps}")
    return travel_steps

def get_final_travel_time(date, time, start, end, get_value):
  trips = None
  if get_value == "here":
    trips = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&itdDate=20200114&itdTime=1200&type_origin=coord&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42&depArrMacro=arr', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})
  elif get_value == "manual":
    trips = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&depArrMacro=dep&itdDate=20200114&itdTime=1200&type_origin=any&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})

  get_json = trips.json()
  journeys = get_json["journeys"]
  # system_messages = get_json["systemMessages"]
  # print(get_json)

  totalDuration = 0
  for journey in get_json["journeys"]:
    legs = journey["legs"]
    for leg in legs:
      totalDuration += leg["duration"]


  return totalDuration

def get_fares(date, time, start, end, get_value):
  trips = None
  if get_value == "here":
    trips = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&itdDate=20200114&itdTime=1200&type_origin=coord&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42&depArrMacro=arr', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})
  elif get_value == "manual":
    trips = requests.get(f'https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&depArrMacro=dep&itdDate=20200114&itdTime=1200&type_origin=any&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42', headers={'authorization': 'apikey i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt'})
  get_json = trips.json()
  # journeys = get_json["journeys"]
  # system_messages = get_json["systemMessages"]
  # print(get_json)

  all_fares = []
  repeat = 0
  counter = 0
  # done = True
  for journey in get_json["journeys"]:
    if repeat == 1:
      break
    fares = journey["fare"]
    for fare in fares["tickets"]:
      person = (fare["person"]).lower()
      all_fares.append(f"{person}: {fare['currency']} ${fare['properties']['priceTotalFare']}")
      counter += 1
      if counter == 4:
        break
    repeat += 1

  return all_fares

#
def get_time():
  now = datetime.now()
  hour = int(now.strftime("%H")) + 11
  minute = int(now.strftime("%M")) + 1
  current_time = now.strftime(f"{hour}{minute}")
  #print(f"Time: {current_time}")
  return current_time
def get_date():
  now = datetime.now()
  current_date = now.strftime(f"%Y%m%d")
  #print(f"Date: {current_date}")
  return current_date

