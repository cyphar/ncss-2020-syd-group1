import requests as req
import json
import os

def setr(key, val, meta, group_path="syd-1", room="", user=""):
  if not room:
    room = meta['room']
  if not user:
    user = meta['author']
  req.post(f"https://store.ncss.cloud/{group_path}/{room}/{user}/{key}", json=val)

def getr(key, meta, group_path="syd-1", room="", user=""):
  if not room:
    room = meta['room']
  if not user:
    user = meta['author']
  r = req.get(f"https://store.ncss.cloud/{group_path}/{room}/{user}/{key}")
  return r.json()

def setl(key, val, meta, group_path="syd-1-events", room="", user=""):
  if not room:
    room = meta['room']
  if not user:
    user = meta['author']
  # # f = open(f'session.json', 'r')
  # conts = getr(key, val, meta, group_path)
  # #f.close()
  # if conts[f'{group_path}&{room}&{user}&session'] is not dict:
  #   conts[f'{group_path}&{room}&{user}&session'] = {}
  # conts[f'{group_path}&{room}&{user}&session'][key] = val
  #f = open(f'session.json', 'w')
  #print(conts)
  #json.dump(conts, f)
  #f.close()
  # setr(key, val, meta, group_path)
  r = req.get(f"https://store.ncss.cloud/{group_path}/{room}/{user}/")
  j = r.json()
  print(j)
  j[key] = val
  req.post(f"https://store.ncss.cloud/{group_path}/{room}/{user}/", json=j)

def dell(meta, group_path="syd-1-events", room="", user=""):
  if not room:
    room = meta['room']
  if not user:
    user = meta['author']
  ##if not os.path.exists('sessions/{group_path}&{room}&{user}&session.json')
  ##  os.mknod('sessions/{group_path}&{room}&{user}&session.json')
  # f = open(f'session.json', 'r')
  # j = json.load(f)
  # f.close()
  # f = open(f'session.json', 'w')
  # j[f'{group_path}&{room}&{user}&session'] = {}
  # print(j)
  # json.dump(j, f)
  # f.close()
  # print(f"https://store.ncss.cloud/{group_path}/{room}/{user}/")
  req.post(f"https://store.ncss.cloud/{group_path}/{room}/{user}/", json={})

def getl(key, meta, group_path="syd-1-events", room="", user=""):
  if not room:
    room = meta['room']
  if not user:
    user = meta['author']
  r = req.get(f"https://store.ncss.cloud/{group_path}/{room}/{user}/")
  j = r.json()
  # print(j)
  return j[key]


