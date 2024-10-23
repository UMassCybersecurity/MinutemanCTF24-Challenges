/*
author: leon
compile: gcc -Og -g -Wall -o wormhole -no-pie src.c
*/
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

int wormhole() {
    char* flag = getenv("flag");
    if (flag == NULL) {
        puts("No flag :(");
        puts("Contact admin");
    }
    puts(flag);
    return 0;
}

int main() {
    puts("The Endurance spaceship needs to jump through the wormhole to find another planet");
    puts("Can you tell the navigation system where the wormhole is?");
    char buf[8] = {0};
    scanf("%5s",buf);
    printf(buf);
    puts("Cool! Let's go towards the wormhole!");
    scanf("%s", buf);
    return 0;
}