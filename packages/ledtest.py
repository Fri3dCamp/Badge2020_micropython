from machine import Pin
from neopixel import NeoPixel


pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, 5)
np[0] = (255, 255, 255)
np[1] = (255, 255, 255)
np[2] = (255, 255, 255)
np[3] = (255, 255, 255)
np[4] = (255, 255, 255)
np.write()