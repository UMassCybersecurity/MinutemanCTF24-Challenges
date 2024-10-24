/*
author: leon
compile: gcc -Oz -no-pie -fno-stack-protector -o trinity-test src.c
*/
#include <stdint.h>
#include <stdio.h>
const char trinity[] = { 0x10, 0x2, 0x12, 0x42, 0x4, 0x1e, 0x5f, 0xd };

long check_activation_code(char* inp);
long check_activation_code(char* inp) {
    register unsigned int part1 = 0x898A9396; // vuli BITWISE NOT
    register unsigned int part2 = 0xDE899A8D; // !ver BITWISE NOT
    unsigned long sum = 0;
    for (long i = 0; i < 4; i++) {
        sum += (~inp[i]) ^ (char)(part1 & 0xff);
        sum += (~inp[i + 4]) ^ (char)(part2 & 0xff);
        part1 >>= 8;
        part2 >>= 8;
    }
    return sum;
}

int main() {
    char inp[8] = { 0 }; // iluvrev!
    puts("enter the activation code:");
    scanf("%8s", &inp);
    register char sum = check_activation_code(inp);
    if (sum!=0) {
        puts("Wrong activation code!");
        return sum;
    }
    for (char i = 0; i < 8; i++) {
        putchar(trinity[i] ^ inp[7 - i]);
    }
    puts("");

    return 0;
}