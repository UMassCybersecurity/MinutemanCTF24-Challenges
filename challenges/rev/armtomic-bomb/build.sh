#! /bin/bash

gcc -Wall -o static/armtomic-bomb-x86-64 -fno-compare-elim -no-pie -fno-stack-protector -fno-omit-frame-pointer src.c
arm-none-eabi-gcc -Wall -o static/armtomic-bomb-armv7 -fno-compare-elim -no-pie -fno-stack-protector -fno-omit-frame-pointer src.c