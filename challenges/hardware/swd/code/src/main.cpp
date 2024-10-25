#include <Arduino.h>

char password[64] = {0};


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if(!strcmp(password, "MINUTEMAN{DebuGgInG_is_C0oL}"))
    digitalWrite(LED_BUILTIN, HIGH); 
}

