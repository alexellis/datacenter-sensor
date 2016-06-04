import time
from reporter import Reporter

r = Reporter("localhost", "6379")

def on_sensor_data(channel, data):
    print(channel, data)
    print(str(r.get_key(data+".temp")))

r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
