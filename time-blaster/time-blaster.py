# time blaster support

from machine import Pin
import time
import _thread
import sys

blaster_link = Pin(4, Pin.IN)

buffer = []

def capture():
    while True:
        start = time.ticks_us()
        buffer.append(blaster_link.value())
        delta = time.ticks_diff(time.ticks_us(), start)
        time.sleep_us(562-delta)

capture_thread = _thread.start_new_thread(capture, ())

def print_blaster_data(data):
    table = ".1"
    print(''.join(table[bit] for bit in data))
    print()

while True:
    try:
        old_buffer = buffer
        buffer = []
        print_blaster_data(old_buffer)
        time.sleep(1)
    except KeyboardInterrupt:
        print("Bye")
        sys.exit()
