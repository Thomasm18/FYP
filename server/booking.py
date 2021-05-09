import requests, json
import time
import datetime
from server import db
from server.api import appid
from server.models import User, Booking
from sqlalchemy import and_
from flask_login import current_user

cloudCover = [0]*8
slots = [1]*8
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

    # To grey out slots that have past
    past_hours = 0 if current_hour < 9 or current_hour>16 else current_hour-9
    for i in range(past_hours):
        slots[i] = 0

    # Change date to tomorrow after 5PM
    if current_hour >16:
        global booking_date 
        booking_date = datetime.date.today() + datetime.timedelta(days = 1)

    # API
    lat = 10.7589
    lon = 78.8132
    exclude = 'current,minutely,daily,alerts'
    units = 'metric'
    endpoint = 'https://api.openweathermap.org/data/2.5/onecall?' \
    + 'lat=' + str(lat) \
    + '&lon=' + str(lon) \
    + '&exclude='+ exclude \
    + '&units=' + units \
    + '&appid=' + appid
    r = requests.get(endpoint)
    r = json.loads(r.content)


    timezone_offset = r["timezone_offset"]

    # Get Hourly weather information
    for i in range(25):
        t = int(datetime.datetime.utcfromtimestamp(r["hourly"][i]["dt"] + timezone_offset).strftime('%H'))
        print(str(datetime.datetime.utcfromtimestamp(r["hourly"][i]["dt"] + timezone_offset).strftime('%H:%M')))
        if (t>=9 and t<=16) and past_hours <8:
            cloudCover[past_hours] = r["hourly"][i]["clouds"]
            past_hours += 1
            print("Time: " + str(t) + ":00")
            print("Cloud Cover: " + str(r["hourly"][i]["clouds"]))

    powerGenerated = getPowerGenerated(cloudCover)
    powerAvailable = getPowerRemaining(powerGenerated)
    costArray = getCostArray(powerAvailable)
    print("Power Generated: " + str(powerGenerated))
    print("Power Available: " + str(powerAvailable))
    print("Cost: " + str(costArray))

    for i in range(len(costArray)):
        # If Available Solar Energy is less that half of what is required during Peak Hours 
        # or Slot not available
        if((i<3 and powerAvailable[i] <= current_user.battery/2) or slots[i] == 0):
            table[i]['available'] = False
            table[i]['cost'] = 'N/A'
            table[i]['saving'] = 'N/A'

        else:
            table[i]['available'] = True 
            table[i]['cost']= round(costArray[i],2)
            table[i]['saving'] = round((current_user.battery*6.6) - costArray[i],2)
    return(table)


def getPowerGenerated(cloudCover):
    powerGenerated = []
    for i in range(len(cloudCover)):
        # Formula for Power Generated based on Cloud Cover
        power = 15*(1-.75*(cloudCover[i]/100)**3)
        powerGenerated.append(round(power,2))
    return powerGenerated

def getPowerRemaining(powerGenerated):
    powerRemaining = []
    for i in range(len(powerGenerated)):
        booking_time = str(i+9)
        bookedSlots = Booking.query.filter(and_(Booking.date == booking_date),(Booking.time == booking_time)).all()
        # If slot has been booked before
        if bookedSlots:
            totalEnergyConsumed = 0
            for slots in bookedSlots:
                chargeUntil = slots.charge_until
                batteryCapacity = slots.user.battery
                totalEnergyConsumed += batteryCapacity * chargeUntil/100
            powerRemaining.append(round(max(0,powerGenerated[i]-totalEnergyConsumed),2))
        else:
            powerRemaining.append(powerGenerated[i])
    return powerRemaining

def getCostArray(powerRemaining):
    costArray = []
    batteryCapacity = current_user.battery
    for i in range(len(powerRemaining)):
        # If Sufficient power is available to charge the vehicle
        if batteryCapacity <= powerRemaining[i]:
            cost = 3.4 * batteryCapacity
        else:
            cost = 3.4 * powerRemaining[i] + 6 * (batteryCapacity - powerRemaining[i])
        costArray.append(round(cost,2))
    return costArray 


def bookSlots(id, chargeUntil):
    # Add Entry into the Booking Table
    booking_time = str(id+9)
    booking = Booking(time = booking_time, date=booking_date, charge_until = chargeUntil, user_id=current_user.id, )
    db.session.add(booking)
    db.session.commit()
    print("Slot Booked on " + str(booking_date) + " for " + booking_time + ":00 till " + str(chargeUntil) + "% charge")
    # Update Port Status
    ports_status = Booking.query.filter(and_(Booking.date == booking_date),(Booking.time == booking_time)).all()
    # If all for ports are booked, slot is full
    if len(ports_status) >= 4:
        slots[id] = 0
    return(str(1))