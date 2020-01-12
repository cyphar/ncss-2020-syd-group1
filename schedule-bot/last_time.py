from datetime import datetime, timedelta
import requests, vobject

# How long since you have been outside?
def last_time(url):
    ical = requests.get(url)
    # parse the top-level event with vobject
    cal = vobject.readOne(ical.text)
    now = datetime.now()+timedelta(hours=11)
    date_now = now.date()

    day_diff = float("inf")
    for component in cal.vevent_list:
        event_date = component.dtstart.value.date()
        print(event_date)

        temp_day_diff = (date_now - event_date).days
        if temp_day_diff < day_diff and (temp_day_diff >= 0):
            day_diff = temp_day_diff

    if day_diff == float("inf"):
        return "You've never been outside"
    elif day_diff == 0:
        return f'Yay! You went out today!'
    elif day_diff == 1:
        return f"You haven't been outside in a day."
    elif day_diff > 1 and day_diff < 6:
        return f"It has been {day_diff} days since you last went outside. Maybe you should go outside!"
    elif day_diff > 6:
        return f"You haven't been outside in {day_diff} days! Please go outside!!!"
    else:
        return f"Error in calculating last time"

