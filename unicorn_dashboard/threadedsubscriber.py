import threading

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
