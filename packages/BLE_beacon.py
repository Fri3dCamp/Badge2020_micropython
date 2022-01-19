# BLE Beacon for the Fri3dcamp 2020 badge

import machine
from micropython import const
import ubluetooth

bt = ubluetooth.BLE()

def adv_encode(adv_type, value):
    return bytes((len(value) + 1, adv_type)) + value


def adv_encode_name(name):
    return adv_encode(const(0x09), name.encode())


def adv():
    bt.gap_advertise(3 * 1000000, adv_encode(0x01, b'\x06')
                     + adv_encode_name('HelloFri3d'))


MAC_OFFSET = 2

def get_mac_address():
    base_mac_address = machine.unique_id()
    mac_address = list(base_mac_address[:-1])
    mac_address.append(base_mac_address[-1] + MAC_OFFSET)
    return ':'.join('%02X' % b for b in mac_address)


print('MAC: ' + get_mac_address())

while not bt.active():
    bt.active(True)
adv()
