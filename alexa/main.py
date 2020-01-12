import flask
import requests
import pprint
import re

app = flask.Flask(__name__)


index = 0
response_array = ["Its raining heavily. I would recommend bringing an umbrella.", "The parties always at N C S S", "Only if you have a parachute"]
AVAILABILITY_URL = "https://schedule-bot.thr0waway.repl.co/free-now"

def fake_request(url, text, params):
  r = requests.post(url, json={
    "author": "Aleksa's Alexa",
    "room": "syd-group1-awful-cursed-room-on-fire",
    "text": text,
    "params": params,
    "alexa-flag": True,
  })

  if not r.ok:
    print(r.text)
    return "Sorry, could not service your request."
  else:
    return r.json()["text"]

  got = r.json()

@app.route("/alexa/everything-is-on-fire", methods=["POST"])
def alexa_itsonfire_route():
  global index
  alexa_request = flask.request.get_json()
  request_type = alexa_request['request']['type']

  if request_type == "LaunchRequest":
    text = "Ask me a question."
    end_session = False
  elif request_type == "SessionEndedRequest":
    text = "Bot failed"
    end_session = True
  else:
    request_intent = alexa_request['request']['intent']['name']
    pprint.pprint(alexa_request["request"])

    if request_intent == "AMAZON.FallbackIntent":
      text = "I dont recognise that one."
    elif request_intent == "weather":
      text = fake_request("https://syd1-weather.kayad.repl.co/", "what's the weather?", {})
    elif request_intent == "freeNow":
      text = fake_request("https://schedule-bot.thr0waway.repl.co/free-now", "am i free now", {})
    elif request_intent == "publicHoliday":
      text = fake_request('https://schedule-bot.thr0waway.repl.co/public-holiday', "public holiday?", {})
    elif request_intent == "events":
      text = fake_request("https://Event-bot.alexnichols.repl.co/necsus", "Are their any events on?", {})
    elif request_intent == "whenWhere":
      text = fake_request("https://Event-bot.alexnichols.repl.co/necsus/timeplace", "When is it?", {})
    elif request_intent == "yes":
      text = fake_request("https://Event-bot.alexnichols.repl.co/necsus/affirm", "yes", {})
    elif request_intent == "no":
      text = fake_request("https://Event-bot.alexnichols.repl.co/necsus/deny", "no", {})
    elif request_intent == "travel":
      target = alexa_request["request"]["intent"]["slots"]["target"]["value"]
      text = fake_request("https://ncss-ioutside-travel.goblincode.repl.co/route", f"from Sydney University to {target}", {"start":"Sydney University", "end":target})
    elif request_intent == "getThere":
      text = fake_request("https://ncss-ioutside-travel.goblincode.repl.co/route", f"How do I get there", {"start":"here", "end":"there"})

    end_session = False
    text = re.sub('<.*?>', ' ', text)
    text = re.sub(':D', ' ', text)


  return flask.jsonify({
    "version": "0.1",
    "response": {
      "outputSpeech": {
        "type": "SSML",
        "ssml": f'<speak><voice name="Russell">{text}</voice></speak>',
      },
      "shouldEndSession": end_session,
    }
  })

app.run(host='0.0.0.0')
