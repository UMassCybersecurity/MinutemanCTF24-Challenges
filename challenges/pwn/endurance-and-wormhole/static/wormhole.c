/*
author: leon
compile: gcc -Og -Wall -o wormhole -no-pie wormhole.c
*/
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

int wormhole() {
    int fd = open("./flag.txt", O_RDONLY);
    if (fd < 0) {
        puts("The flag file is missing. Please contact the admin if you are running this on the server.");
        exit(1);
    }
    char flag[64] = {0};
    read(fd, flag, sizeof(flag));
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