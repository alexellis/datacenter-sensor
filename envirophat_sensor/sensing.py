import time
from Adafruit_BME280 import *
from msense import MotionSense

class Sensors:
    def __init__(self):
        self.sensor = BME280(mode=BME280_OSAMPLE_8)
        self.last_temp = self.read()
        self.motion_sense = MotionSense()

    def read(self):
        degrees = self.sensor.read_temperature()
        self.last_temp = degrees
        self.motion = motion_sense.read()

        return {"temp": degrees, "motion":self.motion}
