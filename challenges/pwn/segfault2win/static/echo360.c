/*
author: august
compile: gcc -o echo360 echo360.c -fno-stack-protector
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void sigsegv_handler(int sig) {
    system("/bin/cat flag.txt");
    fflush(stdout);
    exit(1);
}


int main(int argc, char **argv){
    char buf[16];
    signal(SIGSEGV, sigsegv_handler);

    printf("Welcome to Echo360! What recording would you like to view? ");
    gets(buf);
    printf(buf);
    puts("\n");

    return 0;
}