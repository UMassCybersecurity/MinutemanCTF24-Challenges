#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){ 
    char* ptr = malloc(16);
    char* ptr2 = malloc(16);
    char* ptr3 = ptr;
    free(ptr);
    free(ptr2);
    read(0,ptr3,16-1);
    malloc(16);
    malloc(16);
    malloc(16);
}