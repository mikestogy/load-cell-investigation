int diff_conversion() {

  ADMUX |= 0b11001011;
  ADCSRA |= (_BV(ADEN) | _BV(ADSC));
  while (bit_is_set(ADCSRA, ADSC))
    ;

  int low = ADCL;
  int high = ADCH;
  if(high & (1<<1)){              //in differential mode our value is between -512 to 511 (not 0 to 1023). it means we have 9 bits and 10th bit is the sign bit. but because 
    high |= 0b11111110;           //the number of ADCH and ADCL bits are 10, for signed number we dont have repeatition of 1 in "ADCH" byte.
  }                               //so we repeat 1 Ourselves.:) 
  return (high << 8) | low;
}

void setup() {
  Serial.begin(115200);
  while(!Serial);

  TCCR1A = 0;
  TCCR1B &= ~(_BV(CS12) | _BV(CS11) & ~_BV(CS10));
  TCNT1 = 0;

  unsigned int cycles = TCNT1;

  delay(1000);
}

float previous = millis();

int counter = 0;

void loop() {

  Serial.println((String)micros() + " " + diff_conversion());
  counter += 1;
  
}
