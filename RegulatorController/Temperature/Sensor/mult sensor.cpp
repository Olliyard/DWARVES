/* Multiple DS18B20 1-Wire digital temperature sensors with Arduino example code. More info: https://www.makerguides.com */

// Include the required Arduino libraries:
#include "Arduino.h"
#include "OneWire.h"
#include "DallasTemperature.h"


// Define to which pin of the Arduino the 1-Wire bus is connected:
#define ONE_WIRE_BUS A0

// Create a new instance of the oneWire class to communicate with any OneWire device:
OneWire oneWire(ONE_WIRE_BUS);

// Pass the oneWire reference to DallasTemperature library:
DallasTemperature sensors(&oneWire);

int deviceCount = 0;
float tempC;

void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
  // Start up the library:
  sensors.begin();

  // Locate the devices on the bus:
  Serial.println("Locating devices...");
  Serial.print("Found ");
  deviceCount = sensors.getDeviceCount();
  Serial.print(deviceCount);
  Serial.println(" devices");
}

void loop() {
  // Send the command for all devices on the bus to perform a temperature conversion:
  sensors.requestTemperatures();

  // Display temperature from each sensor
  for (int i = 0;  i < deviceCount;  i++) {
    Serial.print("Sensor ");
    Serial.print(i + 1);
    Serial.print(" : ");
    tempC = sensors.getTempCByIndex(i);
    Serial.print(tempC);
    Serial.print(" \xC2\xB0"); // shows degree symbol
    Serial.print("C ");
  }

  Serial.println();
  delay(1000);
}