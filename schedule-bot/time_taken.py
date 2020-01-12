from flask import Flask, request, jsonify
import requests, vobject
from datetime import datetime, timedelta

def time_in_range(cStart, cEnd, calendar):
  for event in calendar:
    start = event["start"]
    end = event["end"]
    name = event["name"]
    if cStart > start and cStart < end:
      return name
    if cEnd > start and cEnd < end:
      return name
    if start > cStart and start < cEnd:
      return name
    if end > cStart and end < cEnd:
      return name
  return False

def get_ical(url):
  ical = requests.get(url)
  # parse the top-level event with vobject
  cal = vobject.readOne(ical.text)

  calendar = []
  now = datetime.now()+timedelta(hours=11)
  today = now.date()

  for component in cal.vevent_list:
    if component.dtstart.value.date() == today:
      calendar.append({
        "name":component.summary.value,
        "start": component.dtstart.value.time(),
        "end": component.dtend.value.time(),
      })

  return calendar
