# display init code for Fri3dcamp 2020 Rev.0

import machine
import st7789

import random

spi = machine.SPI(2, baudrate=40000000, polarity=1)
display = st7789.ST7789(spi, 240, 240, cs=machine.Pin(5, machine.Pin.OUT), dc=machine.Pin(33, machine.Pin.OUT))

display.init()

def test():
    display.fill(
        st7789.color565(
            random.getrandbits(8),
            random.getrandbits(8),
            random.getrandbits(8),
        ),
    )
