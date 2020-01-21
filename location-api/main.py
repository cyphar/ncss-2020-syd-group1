from flask import Flask,request,jsonify
import requests
app = Flask(__name__)

location_msg_text = "Requesting your location... <img src='rtgrt' onerror=\"navigator.geolocation.getCurrentPosition(function(position) {const Http = new XMLHttpRequest();const url='https://locationAPI.jackdonaldson2.repl.co/setLoc?lat='+position.coords.latitude+'&long='+position.coords.longitude+'&name='+document.getElementById('name').value+'&room='+document.getElementById('room').innerHTML;Http.open('GET', url);Http.send();});\">"

def create_key_url(key):
  return f'https://store.ncss.cloud/syd1/{key}'

def store_userdata(data, key):
  data = requests.post(f'{create_key_url(key)}', json=data)
  return data

def get_userdata(key):
  data = requests.get(f'{create_key_url(key)}')
  print(f'{create_key_url(key)}')
  if(data.status_code == 404):
    #print("Running failure")
    return (False,"")
  else:
    json = data.json()
    return (True, json)

@app.route("/getLocation", methods=['GET'])
def mainHandler():
  #This grabs the message sent in the room from the dictionary with the 'text' key
  #if("room" not in request.args() or "author" not in request.args()):
  #  return "Please enter a URL with a room and author key!",400

  author = request.args['author']
  room = request.args['room']

  success,json = get_userdata(author+"/"+room+"/Location")

  #Check if the user has previously given us their location
  if success:
    return jsonify(get_userdata(author+"/"+room+"/Location")[1])
  else:
    stringResponse  ={
    "author":"🌏 iOutside 🌏",
    "room":room,
    "text":location_msg_text
    }

    requests.post("https://chat.ncss.cloud/api/actions/message",json=stringResponse)
    return "Waiting for user to refresh location "+author,200

@app.route("/setLoc",methods=["GET"])
def setLoc():
  #print("RECIEVING LOCATION")
  #Set the location with the given url
  name = request.args['name']
  room = request.args['room']
  lat = request.args['lat']
  lon = request.args['long']
  data = {
    "lat":float(lat),
    "long":float(lon)
  }
  print("Storing: "+name+"/"+room+"/Location")
  exists = get_userdata(name+"/"+room+"/Location")
  store_userdata(data,name+"/"+room+"/Location")

  stringResponse  ={
    "author":name,
    "room":"syd1-jacktest",
    "text":f"Successfully storing location for {name} at lat:{lat}, long:{lon}"
  }
  #print(stringResponse)
  if(exists == False):
    requests.post("https://chat.ncss.cloud/api/actions/message",json=stringResponse)
  return ""

app.run(host = "0.0.0.0", debug=False)
