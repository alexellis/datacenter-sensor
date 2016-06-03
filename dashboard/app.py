import threading
import redis
import socket
import time

class Reporter:
    def __init__(self, host, port):
       self.host = host
       self.port = port

       self.name = socket.getfqdn()
       self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)
       self.channels = ["sensors.data", "members.add"]

    def find_members(self):
       return self.client.hgetall("members")

    def on_message(self, channel, message):
        print("Channel: "+channel + " - " + message )
        # print(channel, message)

    def set_on_sensor_data(self, cb):
        self.on_sensor_data_cb = cb

    def subscribe(self):
        self.subscriber = ThreadedSubscriber(self.client, self.channels, self.on_sensor_data_cb)
        self.subscriber.run()

class ThreadedSubscriber(threading.Thread):
    def __init__(self, client, channels, callback):
        self.channels = channels
        self.client=client
        self.callback = callback

    def run(self):
        self.pubsub = self.client.pubsub()
        # self.pubsub.subscribe(self.channels)
        self.pubsub.subscribe("sensors.data", "members.add")

        while(True):
            for m in self.pubsub.listen():
                # print m #'Recieved: {0}'.format(m['data'])
                if(m["type"]=="message"):
                    if(self.callback != None):
                        self.callback(m["channel"], m["data"])

r = Reporter("localhost", "6379")

def on_sensor_data(channel, data):
    print channel, data

r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
