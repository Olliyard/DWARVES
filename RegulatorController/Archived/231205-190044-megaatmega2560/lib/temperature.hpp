#pragma once

#include "OneWire.h"
#include "DallasTemperature.h"

// Define to which pin of the Arduino the 1-Wire bus is connected:
#define ONE_WIRE_BUS 53 // D53
#define POWER_PIN 51    // D51

// Create a new instance of the oneWire class to communicate with any OneWire device:
extern OneWire oneWire;

// Pass the oneWire reference to DallasTemperature library:
extern DallasTemperature sensors;

// Function declarations
void temperatureSetup();           // Setup function for temperature sensor
float getTemperature(int colonyID); // Get temperature function
float *getTemperatures();      // Get temperatures function
void testTemperature();            // Test function for temperature sensor
void printAddresses();             // Get addresses function