/*
author: leon
compile: gcc -Oz -no-pie -fno-stack-protector -o trinity-pre-test src.c
*/
#include <stdint.h>
#include <stdio.h>

int main() {
    uint32_t val = 0x8D9A89CE; // rev1 BITWISE NOT

    for (register int i = 0; i < 4; i++) {
        putchar(~val & 0xff);
        val >>= 8;
    }

    return 0;
}