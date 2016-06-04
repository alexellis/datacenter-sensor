from reporting import Reporter
#from sensing import Sensors
from tmp36sensing import Sensors
import time

sensors = Sensors()
reporter = Reporter("localhost", 6379)
reporter.announce()

while(True):
    output = sensors.read()
    print(output)
    reporter.set(output)
    reporter.publish()
    time.sleep(3)
