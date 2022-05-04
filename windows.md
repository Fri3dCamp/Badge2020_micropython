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

## build and flash
* change the USB port in the last 2 lines of build.sh
* ./build.sh
