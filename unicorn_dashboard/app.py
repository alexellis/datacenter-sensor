import time
from reporter import Reporter
import os
import unicornhat as UH
print(os.environ)
#host = os.getenv("REDIS_HOST")
host = os.environ["REDIS_HOST"]
print("Host:" + host)
if(host== None):
    host = "localhost"

UH.clear()
UH.show()

r = Reporter(host, "6379")

def on_sensor_data(channel, data):
    print(channel, data)
    value = float(r.get_key(data+".temp"))
    baseline = float(r.get_key(data+".temp.baseline"))
    print(str(val) + " ~ " + str(baseline))
    diff = abs(val - baseline)

    if(diff < 1):
        UH.set_pixel( 0, 0,178,255,34)
    else:
        UH.set_pixel( 0, 0,178,34,34)

    UH.show()

r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
