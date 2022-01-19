from ctypes import addressof
from machine import Pin
import array
import collections
import sys
import time
import uctypes

pulse_us = 4000
start_pulse = 16
framelength = 8

class Data():

    protocol_descr = {
        "color":    uctypes.BFUINT8 | 0 | 0 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
        "fired":    uctypes.BFUINT8 | 0 | 2 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
        "unused":   uctypes.BFUINT8 | 0 | 3 << uctypes.BF_POS | 4 << uctypes.BF_LEN,
        "parity":   uctypes.BFUINT8 | 0 | 7 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
    }

    def __init__(self) -> None:
        self.bits = bytearray(1)

    def __getitem__(self, n):
        return (self.bits[0] >> n) & 1

    def __setitem__(self, n, v):
        if v:
            self.bits[0] |= v << n
        else:
            self.bits[0] &= ~(1 << n)

    def str_decoded(self):
        data = uctypes.struct(addressof(self.bits), Data.protocol_descr)
        output = 'Data:\n' \
                 '\t color: {}\n' \
                 '\t fired: {}\n' \
                 '\tparity: {}\n'.format(data.color, data.fired, data.parity)
        return output

    def __str__(self):
        return '{:#010b}'.format(self.bits[0])

class Receive:
    frames = collections.deque((), 40)
    buffer = array.array('L')
    micros = 0

    def __init__(self, pin, debug=False):
        self.blaster_link = Pin(pin, Pin.IN)
        self.blaster_link.irq(self.handle_blaster_irq, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.debug = debug
        print("time-blaster Receive initialised on pin ", pin)

    ### This irq creates frames containing pulse lengths.
    # It's designed to be similar to the output of the ESP32 RMT
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

        data = Data()
        for i in range(len(frame)/2):
            delta0 = frame[i*2]
            delta1 = frame[i*2+1]

            # skip start condition
            if (i == 0):
                continue

            if (delta0*2 < delta1):
                data[8-i] = 1
            else:
                data[8-i] = 0

        return data

    def __iter__(self):
        return self

    def __next__(self):
        try:
            frame = self.frames.popleft()
            if self.debug:
                self.print_blaster_frame(frame)
            return self.decode_blaster_frame(frame)
        except:
            raise StopIteration


def test():
    print("Starting blaster link on pin 4")
    blaster_link = Receive(4)
    print("Starting IR on pin 27")
    ir = Receive(27)
    while True:
        try:
            for data in blaster_link:
                print("< " + str(data))
                # print(data.str_decoded())
            
            for data in ir:
                print("I " + str(data))

            time.sleep(1)
        except KeyboardInterrupt:
            print("Bye")
            sys.exit()

test()