from machine import Pin
import array
import collections
import sys
import time

pulse_us = 4000
start_pulse = 16
framelength = 8

blaster_link = Pin(4, Pin.IN)

frames = collections.deque((), 40)
buffer = array.array('L')
micros = 0

### This irq creates frames containing pulse lengths.
# It's designed to be similar to the ouput of the ESP32 RMT
def handle_blaster_irq(pin):
    global buffer
    global micros
    global count
    delta = time.ticks_diff(time.ticks_us(), micros)
    micros = time.ticks_us()
    if delta > start_pulse*pulse_us:
        # Start detected
        buffer = []
        return

    buffer.append(delta)

    if (len(buffer) == (framelength + 1)*2):
        # full frame received
        frames.append(buffer)
        buffer = []


blaster_link.irq(handle_blaster_irq, Pin.IRQ_FALLING | Pin.IRQ_RISING)

def print_blaster_frame(data):
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

def decode_blaster_frame(frame):
    if (len(frame) != (framelength + 1)*2):
        return

    data = array.array('b')
    for i in range(len(frame)/2):
        delta0 = frame[i*2]
        delta1 = frame[i*2+1]

        # skip start condition
        if (i == 0):
            continue

        if (delta0*2 < delta1):
            data.append(1)
        else:
            data.append(0)

    return data


while True:
    try:
        frame = frames.popleft()
        print_blaster_frame(frame)
        data = decode_blaster_frame(frame)
        print(data)
    except IndexError:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Bye")
        sys.exit()
