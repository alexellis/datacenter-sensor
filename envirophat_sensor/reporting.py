import redis
import socket

class Reporter:
    def __init__(self, host, port):
       self.host = host
       self.port = port

       self.name = socket.getfqdn()
       self.live_expiry = 30

    def set_live(self):
        self.client.setex(self.name+".live", self.live_expiry, "1")

    def announce(self):
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)
        self.set_live()
        self.client.hset("members", self.name, "1")
        self.client.publish("members.add", self.name)

    def set_key(self, key, value):
        print(key,value)
        self.client.set(self.name+"."+key, round(value, 2))

    def set_expiring_key(self, key, value, timeout):
        print(key, value, timeout)

        exists = self.client.setnx(self.name+"."+key, value)
        if(exists == 1):
            self.client.expire(self.name+"."+key, timeout)

    def set(self, values):
        self.set_live()

        self.set_key("temp", values["temp"])
        self.set_expiring_key("temp.baseline", round(values["temp"], 2), 60)
        self.set_key("motion", values["temp"])

    def publish(self):
        self.client.publish("sensors.data", self.name)
