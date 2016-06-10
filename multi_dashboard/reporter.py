from threadedsubscriber import ThreadedSubscriber
import redis
import socket

class Reporter:
    def __init__(self, host, port):
       self.host = host
       self.port = port

       self.name = socket.getfqdn()
       self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)
       self.channels = ["sensors.data", "members.add"]

    def find_members(self):
       members = self.client.hgetall("members")
       live = []

       for member in members:
           if(self.client.get(member+".live")):
               live.append(member)
       return live

    def on_message(self, channel, message):
        print("Channel: "+channel + " - " + message )
        # print(channel, message)

    def set_on_sensor_data(self, cb):
        self.on_sensor_data_cb = cb

    def subscribe(self):
        self.subscriber = ThreadedSubscriber(self.client, self.channels, self.on_sensor_data_cb)
        self.subscriber.run()

    def get_key(self, key):
        return self.client.get(key)
