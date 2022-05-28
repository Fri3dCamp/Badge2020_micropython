## Build steps ##

`git submodule update --init --recursive`

`esp-idf/install.sh esp32`

`./build.sh`

Enjoy

## Windows USB drivers
https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

## WiFi setup
* Connect to badge via Serial, BAUD: 115200
* send CTRL+C
* settings.set("wifi.essid","YourSSIDHere")
* settings.set("wifi.password","YourPASSWORDhere")
* settings.store()
* (reset), can be done with CTRL+D
