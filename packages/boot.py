# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

from machine import SoftI2C, Pin
from lis2hh12 import LIS2HH12, SF_G

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensor = LIS2HH12(i2c, address=0x18, sf=SF_G)
# enable the ACC interrupt to turn on backlight
sensor.enable_act_int()

import settings

if settings.get('BLE-beacon_enabled'):
    import BLE_beacon

if settings.get('wifi_enabled'):
    import wifi
    
import apps.menu