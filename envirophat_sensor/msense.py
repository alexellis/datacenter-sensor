from motion import *

class MotionSense:
    def __init__(self):
        self.buffer = []
        self.lsm = accelcomp()
        self.last_avg = 0

    def read(self):
        buf_len = 5

        threshold = 0.02

        self.lsm.getAccel()
        self.buffer.append(self.lsm.accel[X] + self.lsm.accel[Y] + self.lsm.accel[Z])
        self.buffer = self.buffer[-buf_len:]
        avg = reduce(lambda x, y: x + y, self.buffer) / len(self.buffer)
        diff = abs(avg - self.last_avg)

        movement = 0
        if diff > threshold and diff < 1:
            movement = diff
        self.last_avg = avg
        return movement


if __name__ == '__main__':

    from time import sleep
    sense = MotionSense()

    while True:
        val = sense.read()
        if(val > 0):
            print("Motion")
        time.sleep(0.1)
