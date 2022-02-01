from machine import Pin, Timer
import array
import collections
import sys
import time
import uctypes

pulse_us = 520
start_pulse = 4
framelength = 12

class Data():

    protocol_descr = {
        "color":    uctypes.UINT16 | 0 | 0 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
        "fired":    uctypes.UINT16 | 0 | 2 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
        "unused":   uctypes.UINT16 | 0 | 3 << uctypes.BF_POS | 4 << uctypes.BF_LEN,
        "parity":   uctypes.UINT16 | 0 | 7 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
        "rest": uctypes.UINT16 | 0 | 8 << uctypes.BF_POS | 4 << uctypes.BF_LEN,
    }

    def __init__(self) -> None:
        self.bits = bytearray(4)

    def __getitem__(self, n):
        return (self.bits >> n) & 1

    def __setitem__(self, n, v):
        if v:
            self.bits[n/8] |= v << n%8
        else:
            self.bits[n/8] &= ~(1 << n%8)

    def str_decoded(self):
        data = uctypes.struct(uctypes.addressof(self.bits), Data.protocol_descr)
        output = 'Data:\n' \
                 '\t color: {}\n' \
                 '\t fired: {}\n' \
                 '\tparity: {}\n'.format(data.color, data.fired, data.parity)
        return output

    def __str__(self):
        return '{:#012b}'.format(self.bits)

class RMTItem():

    def __init__(self) -> None:
        self.duration0 = 0
        self.level0 = 0
        self.duration1 = 0
        self.level1 = 0

    def str_decoded(self):
        output = 'RMT:\n' \
                 '\t duration0: {}\n' \
                 '\t level0: {}\n' \
                 '\t duration1: {}\n' \
                 '\t level1: {}\n'.format(self.duration0, self.level0, self.duration1, self.level1)
        return output

# fakes the RMT data and interupts
# https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/rmt.html#
class FakeRMT:
    items = collections.deque((), 80)
    micros = 0

    def __init__(self, pin, callback):
        # IRQ on pin to measure time between edges
        self.blaster_link = Pin(pin, Pin.IN)
        self.blaster_link.irq(self.handle_pin_irq, Pin.IRQ_FALLING | Pin.IRQ_RISING)

        # timer for receive timeout
        self.rmt_tim = Timer(0)
        self.rmt_tim.init(period=int(pulse_us*start_pulse*2/1000), mode=Timer.PERIODIC, callback=self.check_rmt_finished)

        # function to call when completed
        self.callback = callback
        
        self.rmt_item = RMTItem()

        ### This irq creates items containing pulse lengths and levels.
    # It's designed to be similar to the output of the ESP32 RMT
    def handle_pin_irq(self, pin):
        delta = time.ticks_diff(time.ticks_us(), self.micros)
        self.micros = time.ticks_us()

        # filter out to long pulses
        if delta < 0 or delta > pulse_us*start_pulse*2:
            return 

        level = pin.value()
        
        if self.rmt_item.duration0 == 0:
            self.rmt_item.duration0 = delta
            self.rmt_item.level0 = level
            return
        
        self.rmt_item.duration1 = delta
        self.rmt_item.level1 = level

        self.items.append(self.rmt_item)
        self.rmt_item = RMTItem()

    def check_rmt_finished(self, t):
        if self.micros == 0:
            return

        if time.ticks_diff(time.ticks_us(), self.micros) > (pulse_us*start_pulse*2):
            # add the last item if it didn't contain 2nd pulse
            if self.rmt_item.duration0 != 0:
                self.items.append(self.rmt_item)
                self.rmt_item = RMTItem()

            self.micros = 0
            self.callback(self.items)

class Receive:
    frames = collections.deque((), 20)
    
    def __init__(self, pin, debug=False):
        self.blaster_link = FakeRMT(pin, self.handle_rmt_finished)
        self.debug = debug
        self.data = Data()
        self.bit = framelength
        print("time-blaster Receive initialised on pin ", pin)

    def handle_rmt_finished(self, items):
        print('rmt complete')

        print('item count = {}'.format(len(items)))
        while(1):
            try:
                item = items.popleft()
                # print(item.str_decoded())
                self.decode_blaster_frame(item)
            except IndexError:
                return

    def decode_blaster_frame(self, item):
        duration = int(item.duration0 / pulse_us)
        if duration > 3:
            print('S', end='')
            self.bit = framelength
            return

        self.bit = self.bit - 1
        if duration >= 2:
            print('1', end='')
            self.data[self.bit] = 1
        elif (duration  < 2):
            print('0', end='')
            self.data[self.bit] = 0
        else:
            print('E', end='')

        if self.bit == 0:
            self.frames.append(self.data)
            self.data = Data()
            print()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.frames.popleft()
        except:
            raise StopIteration

def test():
    print("Starting blaster link on pin 4")
    blaster_link = Receive(4, debug=True)
    # print("Starting IR on pin 27")
    # ir = Receive(27)
    while True:
        try:
            for data in blaster_link:
                print("< " + str(data))
                print(data.str_decoded())
            
            # for data in ir:
            #     print("I " + str(data))

            time.sleep(1)
        except KeyboardInterrupt:
            print("Bye")
            sys.exit()

test()