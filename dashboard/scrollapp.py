import time
from reporter import Reporter
import os
import scrollphat

host = os.getenv("REDIS_HOST")
if(host== None):
    host = "localhost"

scrollphat.set_brightness(10)

r = Reporter(host, "6379")

def on_sensor_data(channel, data):
    print(channel, data)
    val = float(r.get_key(data+".temp"))
    print(str(val))

    scrollphat.write_string( str(round(val))[:2] )
    scrollphat.update()

r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
