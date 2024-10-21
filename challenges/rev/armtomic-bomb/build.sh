#! /bin/bash

# x86-64
x86_64-linux-gnu-gcc -Wall -o static/armtomic-bomb-x86-64 -no-pie -fno-stack-protector src.c
# arm v7 linux
arm-linux-gnueabihf-gcc -Wall -o static/armtomic-bomb-armv7 -no-pie -fno-stack-protector src.c
# arm v8 linux
aarch64-linux-gnu-gcc -Wall -o static/armtomic-bomb-armv8 -no-pie -fno-stack-protector src.c
