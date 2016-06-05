import time
import unicornhat as UH
import redis

UH.set_pixel( 0, 0,178,34,34)
UH.show()
time.sleep(1.5)
UH.set_pixel( 0, 0,178,255,34)
UH.show()
time.sleep(1.5)
UH.set_pixel( 0, 0,0,255,255)
UH.show()
time.sleep(1.5)
UH.clear()

