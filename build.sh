#!/bin/bash

cd micropython/ports/esp32

cp ../../../st7789_mpy/fonts/truetype/NotoSans_32.py modules
make USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake FROZEN_MANIFEST="" FROZEN_MPY_DIR=$UPYDIR/modulesmake USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake PORT=/dev/ttyUSB0 erase
make USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake PORT=/dev/ttyUSB0 deploy

