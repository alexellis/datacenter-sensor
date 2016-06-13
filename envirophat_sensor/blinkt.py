from dotstar import Adafruit_DotStar

numpixels = 8
​
datapin   = 23
clockpin  = 24

class Blinkt:
	def __init__(self, host):
		self.host = host
		self.strip = Adafruit_DotStar(numpixels, datapin, clockpin)
		strip.begin()
		strip.setBrightness(32)

	def show(self, output):
		# float(output[host + "temp"])
		# float(output[host + "temp.baseline"])

		# if(output[host + "temp"] > )