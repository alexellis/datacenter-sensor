from dotstar import Adafruit_DotStar

numpixels = 8
datapin   = 23
clockpin  = 24

class Blinkt:
    def __init__(self, host):
        self.host = host
        self.strip = Adafruit_DotStar(numpixels, datapin, clockpin)
        self.strip.begin()
        self.strip.setBrightness(32)

        green = self.to_rgb(0,255,0)
        self.show_all(green)
    def to_rgb(self,r,g,b):
        return (g << 16) + (r << 8) + b
    def show(self, colour, pixel):
        self.strip.setPixelColor(pixel, colour)
        self.strip.show()
    def show_all(self, colour):
        for x in range(0,8):
            self.strip.setPixelColor(x, colour)
        self.strip.show()
