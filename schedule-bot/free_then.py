# start_event & end_event
import requests
from datetime import datetime

@app.route("/free-then", methods=['POST'])
def free_then():
  r_obj = {
    "author":"📅 iOutside 📅",
  }
  received = request.get_json()
  room = received["room"]
  user = received["author"]
  response = requests.get(f"https://store.ncss.cloud/syd-1/{room}/{user}/current_topic")


  return response,received
print(response, received)
app.run(debug=True, host='0.0.0.0')
