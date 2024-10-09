#include <Arduino.h>

#include "twimaster.c"

#define EEPROM_ADDR 0xA0

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  i2c_init();
}

void loop() {
  i2c_start(EEPROM_ADDR + I2C_WRITE);
	// eeprom address, in little endian
	i2c_write(0x00);
	i2c_write(0x00);
  i2c_write(0x00);

	i2c_start(EEPROM_ADDR + I2C_READ);
	for (uint32_t i = 0; i < 2550326; ++i) {
		Serial.write(i2c_readAck());
	};

  i2c_stop();
  // Serial.printf("Done!\n");
  while(1){
    delay(100000);
  }
}
