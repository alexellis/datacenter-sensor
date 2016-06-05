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

    def set_key(self, key, value):
        print(key,value)
        self.client.set(self.name+"."+key, value)

    def set_expiring_key(self, key, value, timeout):
        print(key,value,timeout)

        exists = self.client.setnx(self.name+"."+key, value)
        if(exists == 1):
            self.client.expire(self.name+"."+key, timeout)

    def set(self, values):
        self.set_key("temp", values["temp"])
        self.set_expiring_key("temp.baseline", values["temp"], 10)
        self.set_key("motion", values["temp"])

    def publish(self):
        self.client.publish("sensors.data", self.name)
