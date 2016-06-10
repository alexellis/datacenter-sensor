import time
from reporter import Reporter
import os
import unicornhat as UH

UH.set_layout(UH.PHAT)

host = os.environ["REDIS_HOST"]
baseline_threshold = 1.5

if(host== None):
    host = "localhost"

UH.clear()
UH.show()

r = Reporter(host, "6379")

def on(column, r,g,b):
    x = column
    for y in range(0, 4):
        print(str(x) + "," + str(y))
        UH.set_pixel(x, y, r, g, b)
    UH.show()

def safeFloat(motion):
    if motion != None:
        return float(motion)
def is_hot(temp, baseline):
    diff = 0
    if(baseline != None and temp != None):
        baseline = round(float(baseline), 2)
        value = round(float(temp), 2)

        diff = abs(temp - baseline)
    return diff > baseline_threshold

def paint():
    index = 0
    members = r.find_members()
    for member in members:
        temp = r.get_key(member + ".temp")
        baseline = r.get_key(member + ".temp.baseline")
        motion = r.get_key(member + ".motion")
        if safeFloat(motion) > 0:
            on(index, 0, 0, 255)
        elif is_hot(temp, baseline):
            on(index, 255, 0, 0)
        else:
            on(index, 0, 255, 0)
        index = index +1
        


def on_sensor_data(channel, data):
    print(channel, data)
    paint()
    # motion = r.get_key(data+".motion")
    # if(motion != None and float(motion) > 0):
    #     on(0,0,255)
    #     UH.show()
    #     return

    # value = r.get_key(data+".temp")
    # baseline = r.get_key(data+".temp.baseline")
    # print(baseline,value)
    # if(baseline != None and value != None):
    #     baseline = round(float(baseline), 2)
    #     value = round(float(value), 2)

    #     diff = abs(value - baseline)
    #     print(str(value) + " ~ " + str(baseline) + " = " + str(diff))

    #     if(diff < 1.5):
    #         on(0,255,0)
    #     else:
    #         on(255,0,0)

    #     UH.show()


r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
