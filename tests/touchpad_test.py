from machine import TouchPad, Pin
import time

# prv = TouchPad(Pin(33))
nxt = TouchPad(Pin(12))
sel = TouchPad(Pin(14))

while True:
    # prv.read()
    # nxt.read()
    print("nxt = {nxt}, sel = {sel}".format(sel=nxt.read(), nxt=sel.read()))
    time.sleep_ms(50)

