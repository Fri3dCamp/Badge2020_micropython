# Temp sensor driver for AHT10 on Fri3dcamp 2020 badge

from machine import Pin, I2C
import time

AHT10_ADDRESS = 0x38
AHT10_INIT_CMD = 0b11100001
AHT10_TRIGGER_CMD = 0b10101100
AHT10_RESET_CMD = 0b10111010

AHT10_STATUS_BUSY_MASK = 1<<7
AHT10_STATUS_MODE_MASK = 0b11<<5
AHT10_STATUS_CALIBRATED_MASK = 1<<3

def status():
    s = i2c.readfrom(AHT10_ADDRESS, 1)[0]
    print('status: {:#010b}'.format(s))
    print('\t busy: {}'.format((s & AHT10_STATUS_BUSY_MASK) >> 7))
    print('\t mode: {}'.format((s & AHT10_STATUS_MODE_MASK) >> 5))
    print('\t calibrated: {}'.format((s & AHT10_STATUS_CALIBRATED_MASK) >> 3))
    return s

# Get temperature (°C) and relative humidity (%)
def readings():
    data = i2c.readfrom(AHT10_ADDRESS, 6)
    rh_data = data[1]<<12 | data[2]<<4 | data[3]>>4
    rh = rh_data * 100/2**20
    t_data = (data[3] & 0x0F)<<16 | data[4]<<8 | data[5]
    t = ((t_data*200)/2**20)-50
    return t, rh

def busy():
    return bool(status() & AHT10_STATUS_BUSY_MASK)


i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

i2c.scan()

status()


print('writing 0b{0:b}'.format(AHT10_INIT_CMD))
buf = bytearray(3)
buf[0] = AHT10_INIT_CMD
buf[1] = 0x08
buf[2] = 0x00
i2c.writeto(AHT10_ADDRESS, buf)

status()

print('writing 0b{0:b}'.format(AHT10_TRIGGER_CMD))
buf = bytearray(3)
buf[0] = AHT10_TRIGGER_CMD
buf[1] = 0x33
buf[2] = 0x00
i2c.writeto(AHT10_ADDRESS, buf)

while(busy()):
    time.sleep_ms(300)

print('temp: %.2f °C, humidity: %d %%' % readings())
