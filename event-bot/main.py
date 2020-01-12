from flask import Flask, request, jsonify
import random
from ticketmasterapi import ticketmaster
import threading

import preferences as prefs
import genericevents
import store


other = [
  'walk',
  'jog',
  'Feed the birds',
  'Go to the shops',
]
app = Flask(__name__)

curr_event = {}


def asking_what_to_do(text):
  words = text.lower().split()
  return words[0] == 'what' and 'i' in words and 'do' in words

def send_message(data, message):
  return jsonify({
    "text": message,
    "author": "🎉 iOutside 🎉",
    "room": data['room']
  })
def send_blank_message(data):
  return jsonify({
    "author": "🎉 iOutside 🎉",
    "room": data['room']
  })

WHAT_DO_TEXT = [
  "Why don't you try",
  "How about",
  "Would you like",
]

def what_do_message(data):
  events = store.getl('event-list', data)
  index = store.getl('event-index', data)
  if index > len(events):
    store.setl("asking-state", False, data)
    return f"Doesn't look like I can find something to do outside.";

  event = events[index]
  rand_text = random.choice(WHAT_DO_TEXT)

  store.setl("curr-event", event, data)
  current_topic = store.getr("current_topic", data)
  if event.get('api', False):
    current_topic['relevant_location'] = event['current_topic']['relevant_location']
    current_topic['end_time'] = event['current_topic']['end_time']
    current_topic['start_time'] = event['current_topic']['start_time']
  store.setr('current_topic', current_topic, data)
  store.setl("event-index", store.getl("event-index", data)+1, data)
  store.setl("asking-state", True, data)

  return f"{rand_text} {event['name']} {r'<br>'}Does that sound good?"

# Regex to match
# .*([Ee]vents|[Ww]hat('?s| is).*on|anything.*on).*
@app.route('/necsus', methods=['POST'])
def route_main():
  data = request.json
  # generate a local session with the user
  store.dell(data)
  store.setl('test', 100, data)
  # TODO use api
  events_tma = ticketmaster()
  events = events_tma # + genericevents.events
  events.sort(key=lambda e: prefs.preference_score(e, data))
  # store.setl('event-distances', prefs.get_distances(events), data)
  store.setl('event-list', events, data)
  store.setl('event-index', 0, data)
  return send_message(data, what_do_message(data))

@app.route('/necsus/timeplace', methods=['POST'])
def route_time():
  data = request.json
  if store.getl("asking-state", data) == False:
    return send_blank_message(data)
  curr_event = store.getl("curr-event", data)
  if not curr_event:
    return send_message(data, f"I don't know what you are talking about {r'<br>'}")
  if 'time' not in curr_event:
    return send_message(data, f"You can do that whenever you want! :D{r'<br>'}You can go to your nearest {curr_event['location']}! :D")
  return send_message(data, f"It's at {curr_event['place']}{r'<br>'}Make sure to get there at {curr_event['time']}")


@app.route('/necsus/delete', methods=['POST'])
def route_delete():
  # end conversation
  data = request.json
  store.dell(data)
  store.setl("asking-state", False, data)

@app.route('/necsus/affirm', methods=['POST'])
def route_affirm():
  data = request.json
  if store.getl("asking-state", data) == True:
    inc_exp()
    store.setl("asking-state", False, data)
    return send_message(request.json, "Sounds good!")
  return send_blank_message(request.json)

@app.route('/necsus/deny', methods=['POST'])
def route_deny():
  data = request.json
  if store.getl("asking-state", data) == True:
    dec_exp()
    return send_message(request.json, what_do_message(data))
  return send_message(request.json, "")

def inc_exp():
  data = request.json
  exp = store.getr('experience', data, room="__global__")
  event = store.getl('curr-event', data)
  if not event['type'] in exp:
    exp[event['type']] = 0
  else:
    exp[event['type']] += 1
  store.setr('experience', exp, data, room="__global__")

def dec_exp():
  data = request.json
  exp = store.getr('experience', data, room="__global__")
  event = store.getl('curr-event', data)
  if not event['type'] in exp:
    exp[event['type']] = 0
  else:
    exp[event['type']] -= 1
  store.setr('experience', exp, data, room="__global__")

app.run(debug='True', host="0.0.0.0")
