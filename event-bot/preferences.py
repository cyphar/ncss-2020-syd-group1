import store
import requests
import random

# ADVANCED_MACHINE_LEARNING
weights = {"distance": .1, "previous_experience": 5}

def preference_score(event, data):
  return random.random()

  pref_score =  weights['distance'] * distance(event, data) + weights['previous_experience'] * previous_experience(event, data)
  ran = random.random()
  return (pref_score, ran)

def get_distances(events):
  adresses = []
  for e in events:
    if 'current_topic' in e:
      adresses.append(e['current_topic']['relevant_location']['address'])
  ## TODO: get url for transport times
  # post_url = 'https://NCSS-iOutside-Travel.goblincode.repl.co/travel_time_calculator'
  # resp = requests.post(post_url, json = adresses)
  return 1 #resp.json()['destinations']


def distance(event, data):
  distances = store.getl('event-distances', data)
  return distances[event['current_topic']['relevant_location']['address']]

def previous_experience(event, data):
  # {"type1": 3, "type2": -5}
  exp = store.getr('experience', data, room="__global__")
  return exp.get(event.get('type', 'other'), 1)


