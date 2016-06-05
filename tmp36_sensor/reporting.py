import redis
import socket

class Reporter:
    def __init__(self, host, port):
       self.host = host
       self.port = port

       self.name = socket.getfqdn()

    def announce(self):
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)
        self.client.hset("members", self.name, "1")
        self.client.publish("members.add", self.name)

    def set_key(self, key, values):
        self.client.set(self.name+"."+key, values[key])

    def set(self, values):
        self.set_key("temp", values)
        self.set_key("motion", values)

    def publish(self):
        self.client.publish("sensors.data", self.name)
