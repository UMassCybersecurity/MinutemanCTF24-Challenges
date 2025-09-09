/*
author: august, leon
compile: gcc -o number_cruncher number-cruncher.c -no-pie -fno-stack-protector
*/

#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main() {
    int addend_1, addend_2;
    puts("Welcome to Number Cruncher! Please enter two numbers to sum.");
    scanf("%d", &addend_1);
    scanf("%d", &addend_2);

    if (addend_1 < 0 || addend_2 < 0) {
        puts("You can't add negative numbers!");
        return 1;
    }

    if ((addend_1 + addend_2) < 0) {
        puts("Congrats, you passed phase 1!");
    } else {
        puts("Hmm, that's not quite right");
        return 1;
    }

    puts("Phase 2! Please enter one number");
    scanf("%d", &addend_1);

    if (addend_1 > 0) {
        puts("You can't use positive numbers!");
        return 1;
    }

    int res = addend_1 - 1;
    if (res > 0) {
        puts("Congrats, you passed phase 2! Here's your flag:");
        system("cat flag.txt");
    } else {
        puts("Hmm, that's not quite right");
        return 1;
    }
    
    return 0;
}