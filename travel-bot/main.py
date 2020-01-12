from flask import Flask, request, jsonify
import requests
import re
import json
from datetime import datetime
from findStopId import findStopId
from planTrip import planTrip, get_final_travel_time, get_fares
from geopy.geocoders import Nominatim
# import get_time

#https://chat.ncss.cloud/syd-group1-travel
#Use above link as our site chatroom

####   APIs   ####
#https://opendata.transport.nsw.gov.au/dataset/trip-planner-apis
#AUTH KEY: i25pwtutuzr0w9CvjxLbciDOw2Yg4EIWfkjt
#Quota: 60,000 per day
#Rate Limit: 5 per second

#get current time (anyone can use this to get local time)
#Don't DELETE!!!
#--------------------------------------------------------
def get_time():
  now = datetime.now()
  hour = int(now.strftime("%H")) + 11
  minute = int(now.strftime("%M")) + 1
  current_time = now.strftime(f"{hour}{minute}")
  print(f"Time: {current_time}")
  return current_time
def get_date():
  now = datetime.now()
  day = int(now.strftime("%d")) + 1
  current_date = now.strftime(f"%Y%m{day}")
  print(f"Date: {current_date}")
  return current_date
#--------------------------------------------------------

app = Flask(__name__)
##################################################
#######   Euans code that he needs to ORGANISE
#######  seriously what out of this code is actually in use im very confused

def shutdown_server():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
  func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
  shutdown_server()
  dic = {
  'author': '🎉 Hahaha Suckers! 🎉',
  'text': f"Direction's server have been shutdown."
  }
  return jsonify(dic)

@app.route("/planTrip", methods=["POST"])
def planTripURL():
  start = findStopId("Bondi")
  print(f"START: {start}")
  end = findStopId("The Rocks")
  print(f"END: {end}")
  travel_steps = planTrip(get_date(), get_time(),start,end)#parse start and end into brackets

  descriptions = []

  for step in travel_steps:
    method, duration = step
    description = f"{duration} minutes by {method}"
    descriptions.append(description)

  final_description = " then ".join(descriptions)


  dic = {
    'author': 'Trip Planner',
    'text': f'It will take {final_description}.'
  }
  return jsonify(dic)

@app.route("/command_not_registered", methods=["POST"])
def unknown_command():
  echo = request.get_json()
  command = echo["params"]["Unknown"]
  magic = {
    'author': 'Ahhh! I don\'t know what you mean.',
    'text': f'<p style="color:red;"> ‣ You have entered an unkown command: "{command}"<br>Type "help" into the message box to get a list of available user message commands.</p>'
  }
  return jsonify(magic)

@app.route("/help", methods =["POST"])
def user_help():
  dashes = "-" * len("To use iOutside******")
  dic = {
    'author': '❓ iOutside ❓',
    'text': f'<p>If you require help, please look and use the following commands in the below list which have been marked with the following symbol " ‣ ".</p><p>To use iOutside<br>{dashes}<br><br><b>The system is not case sensitive...</b><br>  ‣ Enter sentence such as the following to get travel information: From "location_1" to "location_2"<br>  ‣ Need some help. Enter "help" into the message field.<br>  ‣ Search depending on "weather"<br>  ‣ Find out about events nearby by using the following command in your sentence: "event". To get more information or answer a Bot enter one of the following: yes / no or where / when / detail<br>  ‣ Search depending on how busy a person may be: "Am I busy / free / available"<br>  ‣ Check when you were last outside: "Last Day Outside"<br>  ‣ Check when the next public holiday is: "Public Holiday"</p>'
  }
  return jsonify(dic)


def store_url(room, user, key):
  return f"https://store.ncss.cloud/syd-1/{room}/{user}/{key}"

def store_get(room, user, key):
  url = store_url(room, user, key)
  resp = requests.get(url)
  print(resp.text)
  if resp.ok:
    return resp.json()
  return {}

################################

#link for the google map route (from - to)
##### CURRENTLY BEING MODIFIED TO ADD ROUTE DETAILS FROM TRIP PLANNER
##### STILL WORKS BUT HAS A FEW EXTRA UNNECESSARY LINES THAT WILL BE USED LATER
@app.route("/route", methods=["POST"])
def route():
  userRequest = request.get_json()
  print(userRequest)
  #get params and format spaces for urls
  text = userRequest['text']
  start = userRequest["params"]["start"]
  # start = start.replace(" ", "%20")
  end = userRequest["params"]["end"]
  # end = end.replace(" ", "%20")
  print(f"https://www.google.com/maps/dir/{start}/{end}")
  # print(start, end)

  google_start = start
  google_end = end
  if "NSW" not in start:
    google_start = f"{start}, NSW"
  if "NSW" not in end:
    google_end = f"{end}, NSW"

  #Gets stop Ids for start of trip and ned of trip

  room = userRequest["room"]
  user = userRequest["author"]

  if "alexa-flag" not in userRequest:
    response = requests.get(f'https://locationapi.jackdonaldson2.repl.co/getLocation?room={room}&author={user}')
    response = response.json()
    print(response)
  else:
    response = { "lat": -33.8886, "long": 151.1873}
  geolocator = Nominatim(user_agent=__name__)
  final_here_location = geolocator.reverse(f"{response['lat']}, {response['long']}")
  print(final_here_location.address)

  get_value = "manual"
  url = "https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&depArrMacro=dep&itdDate=20200114&itdTime=1200&type_origin=any&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42"

  start_coord = start
  # start = start.replace("%20", "")
  if start.strip().lower() == "here":
    # start = str(final_here_location)
    start_coord = f'{response["long"]:01.6f}:{response["lat"]:01.6f}:EPSG:4326'
    print(start_coord)
    get_value = "here"
    url = "https://api.transport.nsw.gov.au/v1/tp/trip?outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&itdDate=20200114&itdTime=1200&type_origin=coord&name_origin={start}&type_destination=any&name_destination={end}&calcNumberOfTrips=1&TfNSWTR=true&version=10.2.1.42&depArrMacro=arr"

  if end.strip().lower() == "there":
    current_topic = store_get(room, user, "current_topic")
    if "address" not in (current_topic.get("relevant_location") or {}):
      current_topic = { "relevant_location": { "address": "The University of Sydney" } }
    end = current_topic["relevant_location"]["address"]

  print(url)

  start_ID = findStopId(start)
  print(f"START: {start}")
  print(f"start_ID: {start_ID}")
  # end = end.replace("%20", "")
  end_ID = findStopId(end)
  print(f"END: {end}")
  print(f"end_ID: {end_ID}")

  #Plan Trip
  if start.strip().lower() == "here":
    travel_steps = planTrip(get_date(), "1200", start_coord, end_ID, get_value)#parse start and end into brackets
  else:
    travel_steps = planTrip(get_date(), "1200", start_ID, end_ID, get_value)#parse start and end into brackets

  descriptions = []
  times = []
  total_times = {}

  for step in travel_steps:
    method, duration = step
    if method not in total_times:
      total_times[method] = 0
    total_times[method] += duration
    times.append(duration)
    description = f"{duration} minutes by {method}"
    descriptions.append(description)

  main_method = sorted(total_times, key=lambda k: -total_times[k])
  if main_method:
    main_method = main_method[0]
  else:
    main_method = "Walk"
  print("lol, this code is fun:", main_method)

  final_description = " then ".join(descriptions)

  add_times = 0
  for item_based_time in times:
    add_times += int(item_based_time)

  text = None
  if "alexa-flag" in userRequest:
    text = f'Best mode of transportation is by {main_method}, taking {add_times} minutes.'
  elif get_value == "manual":
    travel_fares = get_fares(get_date(), "1200", start_ID, end_ID, get_value)
    long_string = ""
    for fare in travel_fares:
      long_string = long_string+ f"<br>{fare}"

    text = f'<img src="https://cdn.shortpixel.ai/client/q_glossy,ret_img,w_577/https://www.konfest.com/wp-content/uploads/2019/05/Konfest-PNG-JPG-Image-Pic-Photo-Free-Download-Royalty-Unlimited-clip-art-sticker-icon-gps-locate-google-website-search-engine-information-map.png" width=20></img><a target="_blank" href="https://transportnsw.info/trip#/?from={start_ID}&to={end_ID}">Directions.</a><br>It will take {final_description}.<br><br><b>Final Destination Time: </b>{add_times} minutes<br><br><b>Metro Fares</b>{long_string}'
  else:
    text = f'<img src="https://cdn.shortpixel.ai/client/q_glossy,ret_img,w_577/https://www.konfest.com/wp-content/uploads/2019/05/Konfest-PNG-JPG-Image-Pic-Photo-Free-Download-Royalty-Unlimited-clip-art-sticker-icon-gps-locate-google-website-search-engine-information-map.png" width=20></img><a style=color: #f54b42; text-decoration: none; target="_blank" href="https://transportnsw.info/trip#/?from={final_here_location}&to={end_ID}">Directions.</a><br>It will take {final_description}.<br><br><b>Final Destination Time: </b>{add_times} minutes<br>'#<br><b>Metro Fares</b>{long_string}'

  return jsonify({"author": '🗺 iOutside 🗺', "text": text})


#THIS ALLOWS THE EVENTS BOT TO FETCH TRAVEL TIME FOR EACH EVENT
@app.route("/travel_time_calculator", methods=["POST"])
def travel_time_calc():

  destinations = request.get_json()
  print(destinations)
  message = {
    'function': 'Travel Time Calculator',
    'destinations': {}  #{f'{place}':  f'travel_time}'}
  }


  for location in destinations:
    address = location
    print(address)
    Id = findStopId(address)
    Time = int(get_final_travel_time(get_date(), get_time(), findStopId('Bondi'), Id)/60)

    message['destinations'].update({f'{location}': f'{Time}'})

  print(message)
  return jsonify(message)

#HOW DO I GET "THERE"?
@app.route("/get_there", methods=["POST"])
def get_there():
  message = request.get_json()
  room = message["room"]
  user = message["author"]

  print(message)
  response = requests.get(f'http://store.ncss.cloud/syd-1/{room}/{user}/current_topic')
  response = response.json()

  try:
    start_location = response["current_location"]["address"]
  except:
    reply = {
      'author': '🗺 iOutside 🗺🗺',
      'text': "Current location not found",
      }
    return jsonify(reply)

  try:
    relevant_location = response["relevant_location"]["address"]
  except:
    reply = {
      'author': '🗺 iOutside 🗺',
      'text': "No end location specified",
    }
    return jsonify(reply)
  directions = planTrip(get_date(), get_time(), start_location, relevant_location)
  reply = {
    'author': '🗺 iOutside 🗺',
    'text': directions,
    }
  return jsonify(reply)



#Extra code for testing findStopId on NeCSuS
@app.route("/stop_ID", methods=["POST"])
def get_stop_id():
  message = {
    'author': 'Stop ID Bot',
    'text': f'{findStopId("queensland university of technology")}'#any location string
  }
  return jsonify(message)

app.run(debug=False, host="0.0.0.0")

#####Template for what to return to NeCSus: #####
# {'room': 'syd-group1-travel', 'author': 'Anonymous', 'text': 'from blah to blah', 'params': {}}
#################################################
