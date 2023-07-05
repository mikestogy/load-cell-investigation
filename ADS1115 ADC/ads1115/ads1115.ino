#include <Wire.h>

uint16_t data = 0;

void configureADS1115() {
  // Compile write data configure ADS1115
  Wire.beginTransmission(0b01001000);  // Communicate with ADS1115 slave address
  Wire.write(0b00000001);              // Select config register on ADS1115
  Wire.write(0b10001110);              // Configure config register byte 1
  Wire.write(0b11100011);              // Configure config register byte 2
  // Send the configuration data. ADS1115 is now configured
  Wire.endTransmission();
  // Compile write data to request data from ADS1115
  Wire.beginTransmission(0b01001000);
  Wire.write(0b00000000);  // Select conversion data register
  Wire.endTransmission();  // Send the request for data
}

int16_t conversion() {
  // Send read request to ADS1115
  Wire.requestFrom(0b01001000, 2);
  uint8_t MSB = Wire.read();
  uint8_t LSB = Wire.read();
  int16_t data = LSB | (MSB << 8);
  return data;
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000);

  configureADS1115();

  TCCR1A = 0;
  TCCR1B = bit(CS10);
  TCNT1 = 0;

  unsigned int cycles = TCNT1;
  Serial.println((cycles - 1) / 16);

  delay(1000);
}

void loop() {

  Serial.println((String)micros() + " " + (conversion() + 188));
}
