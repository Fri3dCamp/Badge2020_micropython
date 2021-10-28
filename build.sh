#!/bin/bash

cd micropython

make -C mpy-cross

cd ports/esp32

cp ../../st7789_mpy/fonts/truetype/NotoSans_32.py modules

make BOARD=GENERIC_SPIRAM USER_C_MODULES=../../../st7789_mpy/st7789/micropython.cmake FROZEN_MANIFEST="" FROZEN_MPY_DIR=$UPYDIR/modulesmake USER_C_MODULES=../../../../../st7789_mpy/st7789/micropython.cmake PORT=/dev/ttyUSB0 erase
make BOARD=GENERIC_SPIRAM USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake PORT=/dev/ttyUSB0 deploy

cd ../micro-gui
rshell --port /dev/ttyUSB0 cp --recursive gui/ drivers/ /pyboard/

cd ../filesystem
rshell --port /dev/ttyUSB0 --recursive * /pyboard/

