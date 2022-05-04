## install WSL2
* Install "Windows Subsystem for Linux Preview" from windows store
* Install "Ubuntu" from windows store
* Open Ubuntu

## first steps
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install python3-pip cmake
git clone https://github.com/Fri3dCamp/Badge2020_micropython.git
cd Badge2020_micropython/
git submodule update --init --recursive
esp-idf/install.sh esp32

TODO flash
