/*
author: leon
compile: gcc -Oz -no-pie -fno-stack-protector -o trinity-test src.c
*/
#include <stdio.h>

const char trinity[] = { 0x10,0x2,0x12,0x42,0x4,0x1e,0x5f,0xd };

int main() {
    char inp[8] = { 0 }; //iluvrev!
    puts("enter the activation code:");
    scanf("%8s", &inp);
    for (int i = 0; i < 8; i++) {
        putchar(trinity[i] ^ inp[7 - i]);
    }
    puts("");
    
    return 0;
}