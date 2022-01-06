from machine import Pin
import array
import collections
import sys
import time

pulse_us = 4000
start_pulse = 16
framelength = 8

class Receive:
    frames = collections.deque((), 40)
    buffer = array.array('L')
    micros = 0

    def __init__(self, pin):
        self.blaster_link = Pin(pin, Pin.IN)
        self.blaster_link.irq(self.handle_blaster_irq, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        print("time-blaster Receive initialised on pin ", pin)

    ### This irq creates frames containing pulse lengths.
    # It's designed to be similar to the ouput of the ESP32 RMT
    def handle_blaster_irq(self, pin):
        delta = time.ticks_diff(time.ticks_us(), self.micros)
        self.micros = time.ticks_us()
        if delta > start_pulse*pulse_us:
            # Start detected
            self.buffer = []
            return

        self.buffer.append(delta)

        if (len(self.buffer) == (framelength + 1)*2):
            # full frame received
            self.frames.append(self.buffer)
            self.buffer = []

    def print_blaster_frame(self, data):
        for delta in data:
            pulse = (delta/pulse_us)
            if pulse > (start_pulse-1):
                print('H', end='')
            elif pulse > (start_pulse/2 - 1):
                print('L', end='')
            elif pulse < 2:
                print('.', end='')
            elif pulse > 3:
                print('_', end='')

        print()

    def decode_blaster_frame(self, frame):
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


print("Starting blaster link on pin 4")
blaster_link = Receive(4)
while True:
    try:
        frame = blaster_link.frames.popleft()
        blaster_link.print_blaster_frame(frame)
        data = blaster_link.decode_blaster_frame(frame)
        print(data)
    except IndexError:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Bye")
        sys.exit()
