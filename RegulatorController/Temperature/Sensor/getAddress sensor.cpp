/* Multiple DS18B20 1-Wire digital temperature sensors with Arduino example code. More info: https://www.makerguides.com */

// Include the required Arduino libraries:
#include "Arduino.h"
#include "OneWire.h"
#include "DallasTemperature.h"

// Define to which pin of the Arduino the 1-Wire bus is connected:
#define ONE_WIRE_BUS 51
void printTemperature(DeviceAddress address);

// Create a new instance of the oneWire class to communicate with any OneWire device:
OneWire oneWire(ONE_WIRE_BUS);

// Pass the oneWire reference to DallasTemperature library:
DallasTemperature sensors(&oneWire);

// Addresses of DS18B20 sensors connected to the 1-Wire bus
byte sensor1[8] = {0x10, 0xB4, 0xC9, 0x9A, 0x03, 0x08, 0x00, 0x99};
byte sensor2[8] = {0x10, 0x7C, 0x1C, 0x9A, 0x03, 0x08, 0x00, 0x2B};
byte sensor3[8] = {0x10, 0xBF, 0xD4, 0x9A, 0x03, 0x08, 0x00, 0xF1};

void setup()
{
    digitalWrite(53, HIGH); // Set the power pin HIGH to power the DS18B20
    // Begin serial communication at a baud rate of 9600:
    Serial.begin(9600);
    // Start up the library:
    sensors.begin();
    // Set the resolution for all devices to 9, 10, 11, or 12 bits:
    sensors.setResolution(12);

    // Or to: Set the resolution of a specific device to 9, 10, 11, or 12 bits:
    // sensors.setResolution(sensor1, 9);
}

void loop()
{
    // Send the command for all devices on the bus to perform a temperature conversion:
    sensors.requestTemperatures();

    Serial.print("Sensor 1: ");
    printTemperature(sensor1); // call the printTemperature function with the address of sensor1 as input
    Serial.print("Sensor 2: ");
    printTemperature(sensor2);
    Serial.print("Sensor 3: ");
    printTemperature(sensor3);

    Serial.println(); // prints an empty line
    delay(1000);
}

void printTemperature(DeviceAddress address)
{
    // Fetch the temperature in degrees Celsius for device address:
    float tempC = sensors.getTempC(address);
    Serial.print(tempC);
    Serial.print(" \xC2\xB0"); // shows degree symbol
    Serial.print("C\n");
}