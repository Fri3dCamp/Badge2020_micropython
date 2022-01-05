from machine import Pin
import time
import _thread
import sys

pulse_us = 4000
start_pulse = 16

blaster_link = Pin(4, Pin.IN)

buffer = []

micros = 0
def handle_blaster_irq(pin):
    global buffer
    global micros
    delta = time.ticks_diff(time.ticks_us(), micros)
    micros = time.ticks_us()
    if delta > start_pulse*pulse_us:
        buffer = []
        return
    buffer.append(delta)

blaster_link.irq(handle_blaster_irq, Pin.IRQ_FALLING | Pin.IRQ_RISING)

def print_blaster_data(data):
    for delta in data:
        pulse = (delta/pulse_us);
        if pulse > (start_pulse-1):
            print('H', end='')
        elif pulse > (start_pulse/2 - 1):
            print('L', end='')
        elif pulse < 2:
            print('.', end='')
        elif pulse > 3:
            print('_', end='')

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
