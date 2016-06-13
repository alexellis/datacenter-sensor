from reporting import Reporter
from sensing import Sensors
from blinkt import Blinkt

import time
import os

host = os.getenv("REDIS_HOST")
if(host== None):
    host = "redis"

sample_rate = 0.25

sensors = Sensors()
reporter = Reporter(host, 6379)
reporter.announce()

while(True):
    output = sensors.read()
    print(output)
    reporter.set(output)
    reporter.publish()

    blinkt.show(output)

    time.sleep(sample_rate)
