from flask import Flask,request,jsonify
import requests
import time
from datetime import datetime
import pytz
app = Flask(__name__)

def get_weather(username):
  #Gets local weather for Sydney
  #KEY: 9446ff71789295db0526d6f7f2d47a35

  #r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={user_location_data['lat']}&lon={user_location_data['long']}&units=metric&appid=9446ff71789295db0526d6f7f2d47a35")
  r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id=6619279&units=metric&appid=9446ff71789295db0526d6f7f2d47a35")

  #Turn json result into dictionary
  dic = r.json()

  dic['HasPrecipitation'] = False

  if('rain' in dic):
    if('3h' in dic['rain']):
      if(dic['rain']['3h'] > 0.5):
        dic['HasPrecipitation'] = True

  #Return current weather text
  return dic

def get_pollution():
  #Gets local pollution for Sydney
  #KEY:
  pollution = requests.get("https://api.airvisual.com/v2/city?city=Sydney&state=New%20South%20Wales&country=Australia&key=4eceaf77-1c03-44fd-8849-668b3baf7aed")

  #Turn json result into dictionary
  dic2 = pollution.json()

  #Return current weather text
  return dic2


def get_forecast():
  #Gets local uv for Korea
  #KEY:
  forecast = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat=-33.86&lon=151.20&appid=9446ff71789295db0526d6f7f2d47a35&units=metric")

  #Turn json result into dictionary
  dic_forecast = forecast.json()

  #Return current uv text
  return dic_forecast


def get_uv():
  #Gets local uv for Korea??
  #KEY:
  uv = requests.get("https://api.openweathermap.org/data/2.5/uvi?lat=-33.867779&lon=151.208435&appid=9446ff71789295db0526d6f7f2d47a35")

  #Turn json result into dictionary
  dic_uv = uv.json()

  #Return current uv text
  return dic_uv

def forecast_time(current_timestamp):
  call_forecast = get_forecast()
  call_forecast['list']
  for i in call_forecast['list']:
    if current_timestamp > i['dt']:
      forecast_weather = i['weather'][0]['main']
      forecast_temperature = round(i['main']['temp']-273)
      i['HasPrecipitation'] = False
      return i

def create_key_url(room,user):
  return f'https://store.ncss.cloud/syd-1/{room}/{user}/current_topic'

def store_userdata(data, room,user):
  data = requests.post(create_key_url(room,user), json=data)
  return data

def get_userdata(url, room, name, is_alexa=False):
  data = requests.get(f'{url}')
  print(url)
  if(data.status_code == 404):
    if not is_alexa:
      location = get_location(room, name)
    else:
      location = {"lat": None, "long": None}
    #CREATE SPECIAL STUFF
    userInfo = {
      "current_location":{
        "lat":location['lat'],
        "long":location['long'],
        "address":None
      },
      "relevant_location":None,
      "start_time":None,
      "end_time":None,
    }
    #print(userInfo)
    store_userdata(userInfo, room, name)
    return False,""
  else:
    json = data.json()
    #print(json)
    return (True, json)

def get_location(room,name):
  stopCrying = True
  while stopCrying:
    url = "https://locationAPI.jackdonaldson2.repl.co/getLocation?room="+room+"&author="+name
    time.sleep(1.75)
    location = requests.get(url)
    if("refresh" not in location.text):
      stopCrying = False
  return location.json()

def get_unix_time():
  syd_timezone = pytz.timezone('Australia/sydney')
  date_time = datetime.now(syd_timezone)

@app.route("/", methods=['POST'])
def mainHandler():
  #Converts the input dictionary to be readable in python, this is given to us by
  #the server and contains information about the message, author and room
  my_json = request.get_json()
  #This grabs the message sent in the room from the dictionary with the 'text' key
  message = my_json['text']
  name = my_json['author']
  room = my_json['room']
  in_alexa = ("alexa-flag" in my_json)

  response = {
      "author": "☁ iOutside ☁",
      "room": my_json['room'],
      "text": ""
    }

  x,y = get_userdata(create_key_url(room,name), room, name, is_alexa=in_alexa)
  startTime = int(time.time())

  #Check if the user has previously given us their location
  #if check_location_exists(my_json['author']):
  #Calls our weather function and returns a dictionary with the current weather info
  weather = get_weather(name)
  uv = get_uv()
  uv = round(uv['value'])
  weather_text = currentWeather(weather['weather'][0])

  if 'there' in message.lower():
    print(y)
    if "start_time" in y:
      if y['start_time'] != None and y['start_time']!= 0:
        print("success")
        startTime = y['start_time']
        weather = forecast_time(startTime)
        weather_text = currentWeather(weather['weather'][0])
  elif 'tomorrow' in message.lower():
    weather = forecast_time(time.time()+(12*60*60))
    weather_text = currentWeather(weather['weather'][0])
    uv = 2
  pollution1 = get_pollution()

  pollution = round(pollution1['data']['current']['pollution']['aqius'])
  #Determine the message to respond depending on the weather

  temperature = round(weather['main']['temp'])


  #forecast1 = get_forecast
  #forecast = round(forecast[][])


  #syd_timezone = pytz.timezone('Australia/sydney')
  #date_time = datetime.now(syd_timezone)
  #print(startTime)
  date_time = datetime.fromtimestamp(startTime)
  str_time = date_time.strftime("%H:%M:%S")
  list_time = str_time.split(':')
  for i in range(len(list_time)):
    list_time[i] = int(list_time[i])
  hour = list_time[0]
  night = False

  accessory_text = ""
  if weather['HasPrecipitation']:
    accessory_text = 'you should bring an umbrella if you go outside! ☔'
  if temperature < 35 or temperature > 5:
    if hour > 21 and hour < 6:
      night = True
    if int(pollution) < 51:
      accessory_text = 'you should go outside! ☀️'
    elif int(pollution) > 51 or int(pollution) < 151:
      accessory_text = 'Due to poor air quality, if you have respiratory issues, stay indoors. Otherwise, enjoy the outdoors!'
    else:
      accessory_text = 'you should stay indoors!'
  else:
    accessory_text = 'you should stay indoors!'

  uv_text=''
  if uv < 3:
    uv_text = '.'
  else:
    uv_text=", it is recommended you slip, slop, slap and pop on a hat."

  #"The weather out is {weather_text}, the temperature is {temperature}°C and the UV index is {uv}{uv_text} {accessory_text}."

  if night:
    response['text'] = f"It is {temperature}°C and {weather_text}. It is nightime, and dark outside, iOutside recommends staying inside."
  else:
    response['text'] = f"It is {temperature}°C and {weather_text} outside. The UV index is {uv}{uv_text} {accessory_text}."
  return response


def currentWeather(weatherObj):
  main = weatherObj['main']
  #desc = weatherObj['description']
  if main == "Clouds":
    return "cloudy"
  elif main == "Rain":
    return "rainy"
  elif main == "Sun":
    return "sunny"

hasIntroduced = ['Welcome to the Weather Bot','necsus']

@app.route("/intro", methods=['POST'])
def intoHandler():
  my_json = request.get_json()

  name = my_json['author']
  text = my_json['text'].lower()
  if("weather" not in text and "☂" not in text and "☔" not in text):
    response = {
      "author": "☁ Welcome to the Weather Bot ☁",
      "room": my_json['room'],
      "text": "Mention the weather and I will determine if it's safe to go outside and what you need to bring!"
    }

    if name not in hasIntroduced:
      hasIntroduced.append(name)
      return response

  return ""

app.run(host = "0.0.0.0", debug=False)
