/*
author: leon
compile: gcc -Wall -o armtomic-bomb -no-pie -fno-stack-protector src.c
*/

#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#include "arch.h"

struct Bomb {
    int p1;
    int p2;
    int p3;
    int p4;
    char solve[22];
};

typedef struct Bomb Bomb;

// char flag[] = "defuz_d4_b1n4ry_b0mb!";

Bomb the_bomb = { -1, -1, -1, -1, 0x0 };

int write_flag() {
    int fd = creat("./flag.txt", S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    if (fd == -1) {
        printf("can not write flag :( %s", strerror(errno));
        return 1;
    }
    write(fd, the_bomb.solve, 21);
    return 0;
}

void phase1(register unsigned int inp1, register unsigned int inp2) {
    the_bomb.p1 = (inp1 * inp2) ^ 0x4600;
    the_bomb.solve[6] = 0xd4 - inp1; // 112
    the_bomb.solve[7] = 0xd4 - inp2; // 160
}

void phase2(register uint64_t a, register uint64_t b) {
    register uint64_t val = 0x5f62316e3472795f;
    for (register int i = 8; i < 8 + 8; i++) {
        register int charac = (val & a) >> (64 - 8); // 0xFF00000000000000
        the_bomb.solve[i] = charac;
        val <<= b; // 8
    }
    the_bomb.p2 = val;
}

void phase3(register uint32_t inp) {
    uint32_t p3_val = 0b01100010001100000110110101100010; // b0mb in ascii

    inp = ~inp; // solve is 0x9DCF929D
    the_bomb.p3 = inp ^ p3_val;
    for (register int i = 19; i > 19 - 4; i--) {
        the_bomb.solve[i] = inp & 0xFF;
        inp >>= 8;
    }
}

void phase4(register char* inp) {
    //    0xDEF757A def'u' 'z'
    register char t1 = inp[0] - 0xd - 87;
    register char t2 = inp[1] - 0xe - 87;
    register char t3 = inp[2] - 0xf - 87;
    the_bomb.p4 = t1 | t2 | t3 | (inp[3] - 0x75) | (inp[4] - 0x7A);
    the_bomb.solve[0] = inp[0];
    the_bomb.solve[1] = inp[1];
    the_bomb.solve[2] = inp[2];
    the_bomb.solve[3] = inp[3];
    the_bomb.solve[4] = inp[4];
}

int main() {
    the_bomb.solve[5] = '_';
    the_bomb.solve[8] = '_';
    the_bomb.solve[15] = '_';
    the_bomb.solve[20] = '!';

    printf("phase 1, input two numbers\n");
    unsigned int p1a = 0;
    unsigned int p1b = 0;
    printf("num 1: ");
    scanf("%u", &p1a);
    printf("num 2: ");
    scanf("%u", &p1b);
        if ((p1a < 0x61 || p1a > 0x7a) || (p1b < 0x30 || p1b > 0x39)) {
        puts("phase 1 input out of range");
        return 1;
    }
    phase1(p1a, p1b);

    printf("phase 2, input two numbers in hex\n");
    uint64_t p2a = 0;
    uint64_t p2b = 0;
    printf("num 1: ");
#if ARM
    scanf("%llx", &p2a);
#else
    scanf("%lx", &p2a);
#endif

    printf("num 2: ");
#if ARM
    scanf("%llx", &p2b);
#else
    scanf("%lx", &p2b);
#endif
    phase2(p2a, p2b);

    printf("phase 3, input a number in hex\n");
    printf("num: ");
    uint64_t p3a = 0;
#if ARM
    scanf("%llx", &p3a);
#else
    scanf("%lx", &p3a);
#endif
    phase3(p3a);

    printf("phase 4, input a string\n");
    char input[5];
    scanf("%5s", input);
    phase4(input);

    if (the_bomb.p1 + the_bomb.p2 + the_bomb.p3 + the_bomb.p4 == 0) {
        puts("Congratulations! You have defused the bomb!\n");
        return write_flag();
    } else {
        puts("BOOM! The bomb has exploded!\n");
    }
    return 0;
}