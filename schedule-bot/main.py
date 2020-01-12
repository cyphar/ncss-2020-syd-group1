from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from datetime import time as time_constructor
import requests

# Our own modules
from public_holiday import public_holiday
from last_time import last_time
from time_taken import time_in_range, get_ical


# Personal chat name: https://chat.ncss.cloud/syd-1-availability
# Group chat name: https://chat.ncss.cloud/ioutside

app = Flask(__name__)
@app.route("/free-now", methods=["POST"])
def free_now():
  r_obj = {
    "author":"📅 iOutside 📅",
  }
  received = request.get_json()
  r_obj["room"] = received["room"]

  if "at" not in received["text"] and "then" not in received["text"]:
    now = datetime.now()+timedelta(hours=11)
    time_now = now.time()
    calendar = get_ical("https://calendar.google.com/calendar/ical/fndkjp4rq991vsabqm086qtppk%40group.calendar.google.com/public/basic.ics")
    name = time_in_range(time_now, time_now, calendar)

    if name:
      r_obj["text"] = f"Right now is taken by {name}"
    else:
      r_obj["text"] = f"Right now is free"

  return jsonify(r_obj)

@app.route("/last-outside", methods=["POST"])
def last_outside():
  r_obj = {
    "author":"📅 iOutside 📅",
  }

  received = request.get_json()
  r_obj["room"] = received["room"]
  r_obj["text"] = last_time("https://calendar.google.com/calendar/ical/fndkjp4rq991vsabqm086qtppk%40group.calendar.google.com/public/basic.ics")
  return jsonify(r_obj)

@app.route("/public-holiday", methods=["POST"])
def holiday_handler():
  r_obj = {
    "author":"📅 iOutside 📅",
  }
  now = datetime.now()+timedelta(hours=11)
  received = request.get_json()
  r_obj["room"] = received["room"]
  name = public_holiday(now)

  if name:
    r_obj["text"] = f"{name} is today."
  else:
    r_obj["text"] = "No public holidays today."

  return jsonify(r_obj)

@app.route("/free-at-time", methods=["POST"])
def free_at_time():
  r_obj = {
    "author":"📅 iOutside 📅",
  }

  now = datetime.now()+timedelta(hours=11)
  received = request.get_json()
  r_obj["room"] = received["room"]
  params = received["params"]
  if params["hour"]:
    hour = int(params["hour"])
  else:
    hour = 0

  if params["mins"]:
    mins = int(params["mins"])
  else:
    mins = 0

  if params["secs"]:
    secs = int(params["secs"])
  else:
    secs = 0

  calendar = get_ical("https://calendar.google.com/calendar/ical/fndkjp4rq991vsabqm086qtppk%40group.calendar.google.com/public/basic.ics")
  test_time = time_constructor(hour, mins, secs)
  print(test_time)
  name = time_in_range(test_time, test_time, calendar)

  if name:
    r_obj["text"] = f"That time is taken by {name}"
  else:
    r_obj["text"] = f"That time is free"

  return jsonify(r_obj)


@app.route("/free-then", methods=['POST'])
def free_then():
  r_obj = {
    "author":"📅 iOutside 📅",
  }
  received = request.get_json()
  r_obj["room"] = received["room"]
  now = datetime.now()+timedelta(hours=11)
  response = requests.get(f'https://store.ncss.cloud/syd-1/{received["room"]}/{received["author"]}/current_topic')

  if (response.status_code == 200) and ("start_time" in response.json()) and ("end_time" in response.json()):
    start_time = datetime.fromtimestamp(response.json()["start_time"]).time()
    end_time = datetime.fromtimestamp(response.json()["end_time"]).time()

    calendar = get_ical("https://calendar.google.com/calendar/ical/fndkjp4rq991vsabqm086qtppk%40group.calendar.google.com/public/basic.ics")
    name = time_in_range(start_time, end_time, calendar)

    if name:
      r_obj["text"] = f"That time is taken by {name}"
    else:
      r_obj["text"] = f"That time is free"
  else:
    r_obj["text"] = "I don't know what you are talking about."

  return jsonify(r_obj)


@app.route("/help", methods =["POST"])
def main_help():
  received = request.get_json()
  dic = {
    'text': f'Try these commands for a more concise list:<br><ul><li>help weαther</li><li>help location</li><li>help schedule</li><li>help еvеnts</li></ul><br><b>Note: </b><p>commands are not case sensitive</p><br><img src="https://i.imgur.com/DvmXEDE.png" style="width: max-width">',
    'author': '❓ iOutside Help ❓',
    'room': received["room"],
  }

  return jsonify(dic)

@app.route("/help-location", methods =["POST"])
def location_help():
  received = request.get_json()
  dic = {
    'author': '❓ iOutside Location Help ❓',
    'text': f'Try these other commands too!<br><ul><li>help</li><li>help weαther</li><li>help schedule</li><li>help еvеnts</li></ul><br><img src="https://i.imgur.com/5j8P8qU.png" style="width: max-width">',
    'room':received["room"],
  }

  return jsonify(dic)

@app.route("/help-weather", methods =["POST"])
def weather_help():
  received = request.get_json()
  dic = {
    'author': '❓ iOutside Weαther Help ❓',
    'text': f'Try these other commands too!<br><ul><li>help</li><li>help location</li><li>help schedule</li><li>help еvеnts</li></ul><br><img src="https://i.imgur.com/ydAaL13.png" style="width: max-width">',
    'room':received["room"],
  }

  return jsonify(dic)

@app.route("/help-schedule", methods =["POST"])
def schedule_help():
  received = request.get_json()
  dic = {
    'author': '❓ iOutside Schedule Help ❓',
    'text': f'Try these other commands too!<br><ul><li>help</li><li>help location</li><li>help weather</li><li>help еvеnts</li></ul><br><img src="https://i.imgur.com/hR9l1UE.png" style="width: max-width">',
    'room':received["room"],
  }

  return jsonify(dic)

@app.route("/help-events", methods =["POST"])
def events_help():
  received = request.get_json()
  dic = {
    'author': '❓ iOutside Events Help ❓',
    'text': f'Try these other commands too!<br><ul><li>help</li><li>help location</li><li>help schedule</li><li>help weather</li></ul><br><img src="https://i.imgur.com/sK5rd6Y.png" style="width: max-width">',
    'room':received["room"],
  }

  return jsonify(dic)


app.run(debug=True, host='0.0.0.0')

