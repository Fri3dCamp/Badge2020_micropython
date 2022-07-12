#!/bin/bash

source esp-idf/export.sh

echo "Cleaning build"
rm -Rf micropython/ports/esp32/build-GENERIC_SPIRAM/

ROOTDIR=`pwd`
cd micropython

make -C mpy-cross

cd ports/esp32
echo $PWD
make BOARD=GENERIC_SPIRAM FROZEN_MANIFEST="$ROOTDIR/manifest.py"
make BOARD=GENERIC_SPIRAM PORT=/dev/ttyUSB0 erase
make BOARD=GENERIC_SPIRAM PORT=/dev/ttyUSB0 deploy
