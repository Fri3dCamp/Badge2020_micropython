# Read and change the configuration of the Fri3dcamp badge

import json

settings_filename = 'settings.json'

default_wifi_settings = {
    'enabled': True,
    'essid': '',
    'password': '',
    'reconnects': -1
}

default_settings = {
    'BLE-beacon_enabled': True,
    'powersave_enabled': True,
    'wifi': default_wifi_settings
}

current_settings = default_settings

def load():
    global current_settings
    try:
        f = open(settings_filename, 'r')
        current_settings = json.load(f)
    except Exception as e:
        print(e)
        raise Exception('Could not read settings')
    finally:
        f.close()

    print('Loaded settings: ' + json.dumps(current_settings))

def store():
    global current_settings
    save(current_settings)

def save(settings):
    f = open(settings_filename, 'w')
    json.dump(settings, f)
    f.close()

    print('Saved settings: ' + json.dumps(settings))

def items():
    global current_settings
    return current_settings.items()

def set(key, value):
    global current_settings
    current_settings[key] = value

def get(key):
    global current_settings
    return current_settings.get(key)

try:
    load()
except Exception as e:
    print(e)
    print('Saving default!')
    save(default_settings)


def main():
    print("Printing settings")
    for key, value in items():
        print('key = {}: value = {}, type = {}'.format(key, value, type(value)))

if __name__ == "__main__":
    main()