#include <Arduino.h>

const int addressA = 2;  // A pin on CD4051 connected to digital pin 2
const int addressB = 3;  // B pin on CD4051 connected to digital pin 3
const int addressC = 4;  // C pin on CD4051 connected to digital pin 4
const int analogOutPin = 9;  // PWM pin connected to the input of CD4051

void setup() {
  pinMode(addressA, OUTPUT);
  pinMode(addressB, OUTPUT);
  pinMode(addressC, OUTPUT);
}

void loop() {
  // Loop through all eight channels
  for (int i = 0; i < 8; ++i) {
    // Set address pins based on the current channel
    digitalWrite(addressA, (i & 0x01) ? HIGH : LOW);
    digitalWrite(addressB, (i & 0x02) ? HIGH : LOW);
    digitalWrite(addressC, (i & 0x04) ? HIGH : LOW);

    // Output PWM signal to the CD4051
    analogWrite(analogOutPin, map(i, 0, 7, 0, 255));
    
    delay(1000);  // Delay for demonstration purposes, adjust as needed
  }
}
