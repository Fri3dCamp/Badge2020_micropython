# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import settings

if settings.get('BLE-beacon_enabled'):
    import BLE_beacon

if settings.get('wifi_enabled'):
    import wifi
    
import apps.menu
