import time
import explorerhat

class Sensors:
    def __init__(self):
        self.temp = self.read()

    def read(self):
        v1 = explorerhat.analog.four.read()
        celcius = 25 + (v1-0.75) * 100
        self.temp = celcius
        return {"temp": self.temp, "motion":1}
