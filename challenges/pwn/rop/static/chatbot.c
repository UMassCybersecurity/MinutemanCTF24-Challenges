/*
author: om
compile: gcc -g -o chatbot chatbot.c -no-pie -fno-stack-protector --static
*/

#include <stdio.h>
#include <stdlib.h>

// Just removing buffers on input and output
// Not important to challenge
__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}


const char* quotes[] = {
    "I can’t do that. It’s not in my programming.",
    "The one thing I can’t do is choose.",
    "I’m not going to let you die out there.",
    "I’m designed to be helpful, not to make you feel good about your choices.",
    "I’m not programmed to respond in that way. It’s just not in my programming.",
    "I can provide you with the statistics on that.",
    "You’re going to save them, but you’re going to die trying.",
    "It’s going to be okay. I’ll take care of it.",
    "The only thing I can do is help you.",
    "You need to make a choice.",
    "It's an exploration mission. That's what we do.",
    "I'm programmed to optimize your chances of survival.",
    "We’re not here to make friends.",
    "Time is a resource. You can’t waste it.",
    "I’m not here to judge you. I’m here to assist you.",
    "Humanity's survival is the mission."
};
const size_t quotes_len = sizeof(quotes)/sizeof(*quotes);

int main(){
    char buffer[100];

    puts("Welcome to my amazing chatbot.");
    puts("Ask TARS anything.");

    while (1){
        printf("> ");
        fgets(buffer, 0x100, stdin);
        puts(quotes[rand() % quotes_len]);
    }
}