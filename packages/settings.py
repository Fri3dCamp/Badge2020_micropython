# Read and change the configuration of the Fri3dcamp badge

import json

settings_filename = '/settings.json'

default_settings = {
    'BLE-beacon_enabled': True,
    'powersave_enabled': True,
    'wifi': {
        'enabled': True,
        'essid': '',
        'password': '',
        'reconnects': -1,
    },
}

current_settings = default_settings

def load():
    global current_settings
    try:
        with open(settings_filename, 'r') as f:
            current_settings = json.load(f)
    except Exception as e:
        print(e, type(e))
        raise Exception('Could not read settings')
    
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
    sub_next = current_settings
    try:
        for k in key.split('.'):
            sub = sub_next
            last_key = k
            sub_next = sub[k]
    except KeyError:
        ...

    sub[last_key] = value

def get(key):
    global current_settings
    sub = current_settings
    try:
        for k in key.split('.'):
            sub = sub[k]
    except KeyError:
        return None

    return sub

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