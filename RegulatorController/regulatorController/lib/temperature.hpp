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

// Functions
void initTemperature(); // Initialize temperature sensor
void getAddress(int colonyID, DeviceAddress& deviceAddress); // Get address for a given colony ID
float getTemperature(DeviceAddress deviceAddress); // Get temperature for a given device address
