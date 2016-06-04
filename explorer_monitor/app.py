from reporting import Reporter
from explorersensing import Sensors
import time
import os

host = os.getenv("REDIS_HOST")
if(host== None):
    host = "localhost"

sensors = Sensors()
reporter = Reporter(host, 6379)
reporter.announce()

while(True):
    output = sensors.read()
    print(output)
    reporter.set(output)
    reporter.publish()
    time.sleep(3)
