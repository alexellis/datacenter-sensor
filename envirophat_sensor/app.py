from reporting import Reporter
from sensing import Sensors
from blinkt import Blinkt

import time
import os
import signal
import sys

host = os.getenv("REDIS_HOST")
if(host== None):
    host = "redis"

baseline_threshold = os.getenv("TEMP_THRESHOLD")
if(baseline_threshold != None):
    baseline_threshold = float(baseline_threshold)
else:
    baseline_threshold = 0.5

quiet = os.getenv("QUIET")
if(quiet!=None):
    quiet = True
else:
    quiet = False

sample_rate = 0.25

sensors = Sensors()
reporter = Reporter(host, 6379, quiet)
reporter.announce()

host = reporter.get_name()
blinkt = Blinkt(host)

def sigterm_handler(_signo, _stack_frame):
    off()
    # reporting.delete_key(host+".live") # too late to handle this, redis may be down.
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

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
        if(quiet == False):
            print("["+str(diff) + "] "+  str(temp_float) + " - " + str(baseline_float))
    return diff > baseline_threshold

def get_status_color(blinkt, output):
    rgb = None
    if safeFloat(output["motion"]) > 0:
        rgb = blinkt.to_rgb(0, 0, 255)
    elif is_hot(output["temp"], output["temp.baseline"]):
    	rgb = blinkt.to_rgb(255, 0, 0)
    else:
    	rgb = blinkt.to_rgb(0, 255, 0)
    return rgb

def off():
    off = blinkt.to_rgb(0, 0, 0)
    for x in range(0, 8):
        blinkt.show(off, x)

def welcome():
    on = blinkt.to_rgb(0, 0, 255)
    for x in range(0, 8):
        blinkt.show(on, x)
        time.sleep(0.2)
    off = blinkt.to_rgb(0, 0, 0)
    for x in range(0, 8):
        blinkt.show(off, x)
        time.sleep(0.1)

def read_write_loop():
    output = sensors.read()
    if(quiet == False):
        print(output)

    reporter.set(output)
    reporter.publish()

    output["temp.baseline"] = reporter.get_key(host + ".temp.baseline")
    if(output["temp.baseline"] == None):
        output["temp.baseline"] = output["temp"]

    color = get_status_color(blinkt, output)
    blinkt.show_all(color)

if(__name__ == "__main__"):
    off()
    welcome()
    try:
        while(True):
            read_write_loop()
            time.sleep(sample_rate)
    except:
        off()
