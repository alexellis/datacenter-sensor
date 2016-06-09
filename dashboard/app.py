import time
from reporter import Reporter
import os

host = os.getenv("REDIS_HOST")
if(host== None):
    host = "redis"

r = Reporter(host, "6379")

def on_sensor_data(channel, data):
    print(channel, data)
    print(str(r.get_key(data+".temp")))
    print(str(r.get_key(data+".motion")))

r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
