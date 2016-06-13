import redis
import socket

class Reporter:
    def __init__(self, host, port):
       self.host = host
       self.port = port

       self.name = socket.getfqdn()
       self.live_expiry = 300

    def get_host(self):
        return self.host

    def get_key(self, key):
        return self.client.get(key)

    def set_live(self):
        self.set_expiring_key("live", "1", self.live_expiry)
        # self.client.setex(self.name+".live", self.live_expiry, "1")

    def announce(self):
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=0)
        self.set_live()
        self.client.hset("members", self.name, "1")
        self.client.publish("members.add", self.name)

    def set_key(self, key, value):
        print(key,value)
        self.client.set(self.name+"."+key, round(value, 2))

    def overset_expiring_key(self, key, value, timeout):
        self.client.set(self.name+"."+key, value)
        self.client.expire(self.name+"."+key, timeout)  

    def set_expiring_key(self, key, value, timeout):
        print(key, value, timeout)

        exists = self.client.get(self.name+"."+key)
        if(exists==None):
            print(key+ ", value=" + str(value))
            self.client.set(self.name+"."+key, value)
            self.client.expire(self.name+"."+key, timeout)

    def set(self, values):
        self.set_live()

        self.set_key("temp", values["temp"])
        self.set_expiring_key("temp.baseline", round(values["temp"], 2), 300)

        self.overset_expiring_key("motion", values["motion"], 5)


    def publish(self):
        self.client.publish("sensors.data", self.name)
