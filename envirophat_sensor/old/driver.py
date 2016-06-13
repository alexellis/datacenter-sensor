from motion import *

if __name__ == '__main__':

    from time import sleep

    buf = []
    buf_len = 5
    last_avg = 0
    threshold = 0.02

    lsm = accelcomp()

    while True:
        lsm.getAccel()
        buf.append(lsm.accel[X] + lsm.accel[Y] + lsm.accel[Z])
        buf = buf[-buf_len:]
        avg = reduce(lambda x, y: x + y, buf) / len(buf)
        diff = abs(avg - last_avg)
        if diff > threshold and diff < 1:
            print("MOTION!", abs(avg-last_avg))
        last_avg = avg

        time.sleep(0.1)

