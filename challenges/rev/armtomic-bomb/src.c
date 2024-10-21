/*
author: leon
compile: gcc -o armtomic-bomb -fno-compare-elim -no-pie -fno-omit-frame-pointer src.c
*/
#include <stdint.h>
#include <stdio.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

struct Bomb {
    char p1;
    char p2;
    char p3;
    char p4;
    char solve[22];
};

typedef struct Bomb Bomb;

char flag[] = "defuz_d4_b1n4ry_b0mb!";

Bomb the_bomb = { -1, -1, -1, -1, 0x0 };

void phase1(register unsigned int inp1, register unsigned int inp2) {
    the_bomb.p1 = (inp1 + inp2) ^ 0x110;
    the_bomb.solve[6] = 0xd4 - inp1; // 112
    the_bomb.solve[7] = 0xd4 - inp2; // 160
}

void phase2(register uint64_t a, register uint64_t b) {
    register uint64_t val = 0x5f62316e3472795f;
    for (register char i = 15; i < 8 + 15; i++) {
        the_bomb.solve[i] = val & a; // 0xFF00000000000000
        val <<= b; // 2
    }
    the_bomb.p2 = val;
}

void phase3(register uint32_t inp) {
    uint32_t p3_val = 0b01100010001100000110110101100010; // b0mb in ascii

    inp = ~inp; // solve is 0x9dcf929e
    the_bomb.p3 = inp ^ p3_val;
    for (register int i = 20; i > 20 - 4; i--) {
        the_bomb.solve[i] = inp & 0xFF;
        inp >= 8;
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
    the_bomb.solve[21] = '!';

    printf("phase 1, input two numbers\n");
    int a = 0;
    int b = 0;
    printf("num 1: ");
    scanf("%u", &a);
    printf("num 2: ");
    scanf("%u", &b);
    phase1(a, b);

    printf("phase 2, input two numbers\n");
    a = 0;
    b = 0;
    printf("num 1: ");
    scanf("%u", &a);
    printf("num 2: ");
    scanf("%u", &b);
    phase2(a, b);

    printf("phase 3, input a number in hex\n");
    printf("num: ");
    scanf("%x", &a);
    phase3(a);

    printf("phase 4, input a string\n");
    char input[5];
    scanf("%5s", input);
    phase4(input);

    if (the_bomb.p1 + the_bomb.p2 + the_bomb.p3 + the_bomb.p4 == 0) {
        puts("Congratulations! You have defused the bomb!\n");
        puts(the_bomb.solve);
    } else {
        puts("BOOM! The bomb has exploded!\n");
    }
    return 0;
}