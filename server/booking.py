import requests, json
import time
import datetime
from server import db
from server.api import appid
from server.models import User, Booking
from sqlalchemy import and_
from flask_login import current_user

solar_radiation = [0]*8
slots = [1,1,1,1,1,1,1,1]
ports_status =[[1]*3]*8
table = []
booking_date = datetime.date.today()


#Create Dictionary TimeTable
for i in range(8):
    if i < 3:
        t = str(i + 9) + " AM"
    elif i == 3:
        t = "12 PM"
    else:
        t = str(i-3) + " PM"
    table.append({'id':i,'time':t, 'cost': 0, 'saving':0, 'available':True})


#Get Slots and Cost
def checkSlots():
    # Check current time
    t = time.localtime()
    current_hour = int(time.strftime("%H", t))

    # To Grey out slots that have past
    past_hours = 0 if current_hour < 9 or current_hour>16 else current_hour-9
    for i in range(past_hours):
        slots[i] = 0

    # Change date to tomorrow
    if current_hour >16:
        global booking_date 
        booking_date = datetime.date.today() + datetime.timedelta(days = 1)

    # API
    lat = 10.7589
    lon = 78.8132
    exclude = 'current,minutely,daily,alerts'
    units = 'metric'
    endpoint = 'https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude='+ exclude + '&units=' + units + '&appid=' + appid
    r = requests.get(endpoint)
    r = json.loads(r.content)
    timezone_offset = r["timezone_offset"]

    for i in range(25):
        t = int(datetime.datetime.utcfromtimestamp(r["hourly"][i]["dt"] - timezone_offset).strftime('%H'))
        if (t>=9 and t<=16) and past_hours <8:
            if r["hourly"][i]["clouds"] < 50:
                solar_radiation[past_hours] = 1
            past_hours += 1
            print("Time: " + str(t) + ":00")
            print("Cloud Cover: " + str(r["hourly"][i]["clouds"]))

    for i in range(len(solar_radiation)):
        # Solar Available and Slots Free
        if(solar_radiation[i]==1 and slots[i]==1):
            table[i]['available'] = True
            table[i]['cost']=10.2
            table[i]['saving'] = 9.6

        # Solar unavailable during non-peak and Slots Free
        elif(i>=3 and slots[i]==1):
            table[i]['available'] = True
            table[i]['cost'] = 18
            table[i]['saving'] = 1.8

        # Solar unavailable during peak or Slots not Free
        else:
            table[i]['available'] = False
            table[i]['cost'] = 'N/A'
            table[i]['saving'] = 'N/A'
    return(table)


def bookSlots(id):
    booking_time = str(id+9)
    booking = Booking(time = booking_time, user_id=current_user.id, date=booking_date)
    db.session.add(booking)
    db.session.commit()
    print("Slot Booked on " + str(booking_date) + " for " + booking_time + ":00")

    # Update Port Status
    ports_status = Booking.query.filter(and_(Booking.date == booking_date),(Booking.time == booking_time)).all()
    if len(ports_status) >= 3:
        slots[id] = 0
    return()