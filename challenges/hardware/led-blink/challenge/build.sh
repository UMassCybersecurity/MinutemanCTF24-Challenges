# This file is used to build the src folder
# Get location of script
ROOT="$(dirname "$(readlink -f "$0")")"

cd $ROOT
echo Building $ROOT...

LIB_PATH=$ROOT/lib/simavr/build

mkdir $ROOT/build

gcc \
 -iquote$ROOT/lib/simavr/src -iquote$ROOT/include \
 -L$LIB_PATH -Wl,-rpath=$LIB_PATH \
 -lsimavr \
 -lm -g $ROOT/src/ctf_challenge.c $ROOT/src/utils.c $ROOT/src/laser_module.c $ROOT/src/custom_i2c_eeprom.c $ROOT/src/uart_file.c $ROOT/src/main.c -o $ROOT/build/main

echo Build done!