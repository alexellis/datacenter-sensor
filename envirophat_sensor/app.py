from reporting import Reporter
from sensing import Sensors
from blinkt import Blinkt

import time
import os

host = os.getenv("REDIS_HOST")
if(host== None):
    host = "redis"

baseline_threshold = os.getenv("TEMP_THRESHOLD")
if(baseline_threshold == None):
    baseline_threshold = 0.5

sample_rate = 0.25

sensors = Sensors()
reporter = Reporter(host, 6379)
reporter.announce()

host = reporter.get_host()
blinkt = Blinkt(host)

def safeFloat(motion):
    if motion != None:
        return float(motion)
    return 0

def is_hot(temp, baseline):
    diff = 0
    if(temp != None and baseline != None):
        baseline_float = round(float(baseline), 2)
        temp_float = round(float(temp), 2)
        diff = abs(temp_float - baseline_float)
        print("["+str(diff) + "] "+  str(temp_float) + " - " + str(baseline_float))
    return diff > baseline_threshold

def get_status_color(blinkt, output):
    rgb = None
    if safeFloat(output["motion"]) > 0:
        rgb = blinkt.to_rgb(index, 0, 0, 255)
    elif is_hot(output["temp"], output["temp.baseline"]):
    	rgb = blinkt.to_rgb(index, 255, 0, 0)
    else:
    	rgb = blinkt.to_rgb(index, 0, 255, 0)
    return rgb

while(True):
    output = sensors.read()
    print(output)
    reporter.set(output)
    reporter.publish()
    output["temp.baseline"] = reporter.get_key(host + "temp.baseline")
    if(output["temp.baseline"] == None):
        output["temp.baseline"] = output["temp"]

    color = get_status_color(blinkt, output)
    blinkt.show_all(color)

    time.sleep(sample_rate)
