import network
from settings import Settings

class Wifi():
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        settings = Settings()
        try:
            self.essid = settings.get('wifi_essid')
            self.password = settings.get('wifi_password')
            self.reconnects = settings.get('wifi_reconnects')
        except Exception as e:
            print("Could not load Wifi settings! " + e)
            

    def do_connect(self):
        self.wlan.active(True)
        if self.wlan.isconnected():
            return
        print('connecting to network...')
        try:
            print("essid = {}, password = {}, reconnects = {}". format(self.essid, self.password, self.reconnects))
            self.wlan.config(reconnects=self.reconnects)
            self.wlan.connect(self.essid, self.password)
        except Exception as e:
            print('Could not connect! ' + e)
        
    def is_connected(self):
        return self.wlan.isconnected()

    def disable(self):
        self.wlan.active(False)

def test():
    import time
    wifi = Wifi()
    wifi.do_connect()

    while wifi.is_connected() == False:
        print('waiting to connect')
        time.sleep(1)
    print('network config:', wifi.wlan.ifconfig())