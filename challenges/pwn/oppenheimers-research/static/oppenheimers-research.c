/*
Compile: gcc o
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

const char prompt[] = "Your password input: ";
const unsigned short prompt_size = sizeof(prompt) - 1;

char* password;
char* flag;

int main(){    
    char is_oppenheimer = 0;
    char buffer[128];
    
    password = getenv("PASSWORD");
    if(password == NULL) {
        puts("No password :(");
        return 1;
    }

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
        puts("Welcome oppenheimer");
        flag = getenv("FLAG");
        if(flag == NULL) {
            puts("No flag :(");
            return 1;
        }
        printf("flag: %s\n", flag);
    }
}