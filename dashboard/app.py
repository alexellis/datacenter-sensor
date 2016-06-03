import redis
import socket
import time

class Reporter:
    def __init__(self, host, port):
       self.host = host
       self.port = port

       self.name = socket.getfqdn()
       self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)
       self.pubsub = self.client.pubsub()
       self.pubsub.subscribe("sensors.data", self.on_message)
       self.pubsub.subscribe("members.add", self.on_message)

    def find_members(self):
       return self.client.hgetall("members")

    def on_message(self, channel, message):
        print(channel, message)

    def set_on_sensor_data(self, cb):
        self.on_sensor_data_cb = cb
    def subscribe():
        self.client

r = Reporter("localhost", "6379")

def on_sensor_data(name):
    print name

r.set_on_sensor_data(on_sensor_data)

while True:
    print (r.find_members())
    time.sleep(5)
