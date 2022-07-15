## install WSL2
* Install "Windows Subsystem for Linux Preview" from windows store
* Install "Ubuntu" from windows store
* Open Ubuntu

## first steps
* sudo apt-get update && sudo apt-get dist-upgrade
* sudo apt-get install python3-pip cmake
* git clone https://github.com/Fri3dCamp/Badge2020_micropython.git
* cd Badge2020_micropython/
* git submodule update --init --recursive
* esp-idf/install.sh esp32

## install tools to USB forward to WSL2
* in windows
  * install https://github.com/dorssel/usbipd-win/releases in windows
* in WSL linux
  * sudo apt install linux-tools-virtual hwdata
  * sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/*/usbip 20

## forward badge USB to WSL
* in windows
  * usbipd wsl list
    * in the list you see you will find a line with "Silicon Labs CP210x USB to UART Bridge" with in the very front of the line a bus ID, in my case 2-1
  * usbipd wsl attach --busid 2-1

## Make a udev rule to give proper permissions and a symbolic link
* plug in your fri3d badge and run the following command `udevadm info -a /dev/ttyUSB0`
  look for the device `ATTRS{product}=="CP2104 USB to UART Bridge Controller"` and look for the `serial` attribute 
* create the following file in /etc/udev/rules.d/61-usb_serial.rules (file owned by root:root 644)
  change the serial for the one found in the command above (or remove the whole ATTRS{serial} part)
```
# Copy this file to /etc/udev/rules.d/61-usb_serial.rules

ACTION!="add|change", GOTO="usb_serial_rules_end"
SUBSYSTEM!="usb|tty", GOTO="usb_serial_rules_end"

# CP201x
ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", ATTRS{serial}=="01C81E54", MODE="660", GROUP="plugdev", TAG+="uaccess", SYMLINK+="fri3dBadge2020"

LABEL="usb_serial_rules_end"
```
* reload the rules `sudo udevadm control --reload`  
  If you get an error "Failed to send reload request: No such file or directory"  
  run `sudo service udev restart` then run `sudo udevadm control --reload` again.
* unplug your badge and plug it in again
* enjoy your personalized /dev/fri3dBadge2020 link

## build and flash
* change the USB port in the last 2 lines of build.sh
* ./build.sh

## error `Failed to connect to ESP32: Timed out waiting for packet header`
if you get the error `Failed to connect to ESP32: Timed out waiting for packet header`  
try the following when the esptool is trying to connect:
```
Serial port /dev/fri3dBadge2020
Connecting...............
```
1. hold the button labeled boot - drukknop - IO00
2. press the reset button  
This will reset the esp32 and hold it in boot mode.  
3. Once the esptool is flashing you can let go of the boot button.
