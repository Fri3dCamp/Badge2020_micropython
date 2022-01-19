import network
import settings

wlan = network.WLAN(network.STA_IF)

try:
    essid = settings.get('wifi_essid')
    password = settings.get('wifi_password')
    reconnects = settings.get('wifi_reconnects')
except Exception as e:
    print("Could not load Wifi settings! " + e)
            

def do_connect():
    wlan.active(True)
    if wlan.isconnected():
        return
    print('connecting to network...')
    try:
        print("essid = {}, password = {}, reconnects = {}". format(essid, password, reconnects))
        wlan.config(reconnects=reconnects)
        wlan.connect(essid, password)
    except Exception as e:
        print('Could not connect! ' + str(e))
    
def is_connected():
    return wlan.isconnected()

def disable():
    wlan.active(False)

def test():
    import time
    do_connect()

    while wifi.is_connected() == False:
        print('waiting to connect')
        time.sleep(1)
    print('network config:', wifi.wlan.ifconfig())

do_connect()