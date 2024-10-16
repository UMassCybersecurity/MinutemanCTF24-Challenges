/*
author: om
compile: gcc -g -o oppenheimers-research oppenheimers-research.c -no-pie -fno-stack-protector
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

const char prompt[] = "Your password input: ";
const unsigned short prompt_size = sizeof(prompt) - 1;

// Just removing buffers on input and output
// Not important to challenge
__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main(int argc, char* argv[]){
    char is_oppenheimer = 0;
    char buffer[128];
    char password[128];

    FILE *passwd = fopen("password.txt", "r");
    if(passwd == NULL) {
        puts("No password :(");
        return 1;
    }
    fgets(password, 128, passwd);

    strcpy(buffer, prompt); //add prompt

    puts("Enter research password:");
    fgets(buffer + prompt_size, 128, stdin);

    buffer[strlen(buffer) - 1] = 0; //remove \n
    puts(buffer);

    if(strcmp(buffer + prompt_size, password) == 0){
        is_oppenheimer = 1;
    } else {
        puts("Incorrect");
    }

    if(is_oppenheimer){
        puts("Welcome oppenheimer!");

        FILE *flag = fopen("flag.txt", "r");
        if(flag == NULL) {
            puts("No flag :(");
            return 1;
        }
        char buff[128];
        fgets(buff, 128, flag);
        printf("flag: %s\n", buff);
    }
}