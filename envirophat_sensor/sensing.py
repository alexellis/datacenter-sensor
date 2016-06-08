import time
from Adafruit_BME280 import *

class Sensors:
    def __init__(self):
        self.sensor = BME280(mode=BME280_OSAMPLE_8)
        self.last_temp = self.read()

    def read(self):
        degrees = self.sensor.read_temperature()
        self.last_temp = degrees

        return {"temp": degrees, "motion":1}
