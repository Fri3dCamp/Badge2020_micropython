# Read and change the configuration of the Fri3dcamp badge

import json

class Settings:

    settings_filename = 'settings.json'

    default_settings = {
        'BLE-beacon_enabled': True,
        'powersave_enabled': True,
        'wifi_enabled': True,
        'wifi_essid': '',
        'wifi_password': '',
        'wifi_reconnects': -1
    }

    def __init__(self):
        self.current_settings = Settings.default_settings
        self.filename = Settings.settings_filename
        try:
            self.load()
        except Exception as e:
            print(e)
            print('Saving default!')
            self.save(Settings.default_settings)

    def load(self):
        try:
            f = open(self.filename, 'r')
            self.current_settings = json.load(f)
        except Exception as e:
            print(e)
            raise Exception('Could not read settings')
        finally:
            f.close()

        print('Loaded settings: ' + json.dumps(self.current_settings))

    def store(self):
        self.save(self.current_settings)

    def save(self, settings):
        f = open(self.filename, 'w')
        f.write(json.dumps(self.default_settings))
        f.close()

        print('Saved settings: ' + json.dumps(settings))

    def items(self):
        return self.current_settings.items()

    def set(self, key, value):
        self.current_settings[key] = value

    def get(self, key):
        return self.current_settings.get(key)

def main():
    print("Printing settings")
    settings = Settings()

    for key, value in settings.items():
        print('key = {}: value = {}, type = {}'.format(key, value, type(value)))

if __name__ == "__main__":
    main()