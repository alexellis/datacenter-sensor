class Sensors:
    def __init__(self):
        self.temp = 10
        self.motion = 1

    def read(self):
        self.motion = self.motion +0.1
        self.temp = self.temp + 0.2
        return {"temp": self.temp, "motion": self.motion}
