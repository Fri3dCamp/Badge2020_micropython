#!/bin/bash

BOARD=FRI3D_BADGE_2020_REV2
SERIAL_PORT=/dev/ttyUSB0

source esp-idf/export.sh

ROOTDIR=`pwd`
cd micropython

make -C mpy-cross

cd ports/esp32
# link our board file into micropython
[ ! -e boards/$BOARD ] && ln -s $ROOTDIR/boards/$BOARD boards/$BOARD

echo $PWD
make BOARD=$BOARD clean
make BOARD=$BOARD FROZEN_MANIFEST="$ROOTDIR/manifest.py"
# make BOARD=$BOARD PORT=$SERIAL_PORT erase
make BOARD=$BOARD PORT=$SERIAL_PORT deploy
