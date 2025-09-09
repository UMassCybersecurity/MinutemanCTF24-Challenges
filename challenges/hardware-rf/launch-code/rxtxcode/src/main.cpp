#include <Arduino.h>
#include <SoftwareSerial.h>

const char message[] = "MINUTEMAN{sEcreT_meSsag3}";
const size_t message_len = sizeof(message) - 1;

SoftwareSerial serial2 = SoftwareSerial(8,9);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  serial2.begin(9600);
}

void loop() {
  Serial.println("Send XOR key for secure communication.");
  serial2.readStringUntil('\n');
  byte key[message_len];
  for(size_t i = 0; i < message_len; i++){
    key[i] = random(256);
  }
  serial2.write(key, message_len);
  Serial.readBytes(key, message_len);
  Serial.println("Send message.");
  serial2.readStringUntil('\n');
  byte enc_message[message_len];
  for(size_t i = 0; i < message_len; i++){
    enc_message[i] = message[i] ^ key[i];
  }
  serial2.write(enc_message, message_len);
  Serial.readBytes(enc_message, message_len);
  Serial.println("Message received.");
  delay(100);
}