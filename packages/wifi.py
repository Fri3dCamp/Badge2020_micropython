import network
import settings

wlan = network.WLAN(network.STA_IF)

try:
    essid = settings.get('wifi', 'essid')
    password = settings.get('wifi', 'password')
    reconnects = settings.get('wifi', 'reconnects')
    print("essid = {}, password = {}, reconnects = {}". format(essid, password, reconnects))
except Exception as e:
    print("Could not load Wifi settings! " + str(e))
            

def do_connect():
    wlan.active(True)
    if wlan.isconnected():
        return
    print('connecting to network...')
    try:
        wlan.config(reconnects=reconnects)
        wlan.connect(essid, password)
    except Exception as e:
        print('Could not connect! ' + str(e))
    
def is_connected():
    return wlan.isconnected()

def disable():
    wlan.active(False)

def status():
    status = wlan.status()
    if status == network.STAT_IDLE:
        return 'idle'
    elif status == network.STAT_CONNECTING:
        return 'connecting'
    elif status == network.STAT_WRONG_PASSWORD:
        return 'wrong password'
    elif status == network.STAT_NO_AP_FOUND:
        return 'no ap found'
    elif status == network.STAT_GOT_IP:
        return 'IP {}'.format(ip())
    
    return 'error'

def ip():
    return wlan.ifconfig()[0]

def test():
    import time
    do_connect()

    while wifi.is_connected() == False:
        print('waiting to connect')
        time.sleep(1)
    print('network config:', wifi.wlan.ifconfig())

do_connect()