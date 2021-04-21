import requests, json
import time
from api import appid
solar_radiation = [0]*8
slots = [1,1,1,1,1,1,1,1]
ports_status =[[1]*3]*8
table = []


for i in range(8):
    if i < 3:
        t = str(i + 9) + " AM"
    elif i == 3:
        t = "12 PM"
    else:
        t = str(i-3) + " PM"
    table.append({'id':i,'time':t, 'cost': 0, 'saving':0, 'available':True})


def checkSlots():
    # Check current time
    t = time.localtime()
    current_hour = int(time.strftime("%H", t))
    past_hours=0
    if current_hour>9:
        past_hours = current_hour-9
    for i in range(past_hours):
        slots[i] = 0

    # # API
    lat = 10.7589
    lon = 78.8132
    exclude = 'current,minutely,daily,alerts'
    units = 'metric'
    endpoint = 'https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude='+ exclude + '&units=' + units + '&appid=' + appid
    r = requests.get(endpoint)
    r = json.loads(r.content)
    for i in range(past_hours,8):
        if r["hourly"][i]["clouds"] < 50:
            solar_radiation[i] = 1
        print( r["hourly"][i]["clouds"])
    # print(solar_radiation)

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
    # Update Port Status
    for i in range(len(ports_status[id])):
        if ports_status[id][i] == 1:
            ports_status[id][i] = 0
            break
    print(ports_status[id])
    # Check is any port is still available
    for num in ports_status[id]:
        if num == 1:
            return()
    # Update slots if no port is available
    slots[id] = 0
    print(slots)
    return()