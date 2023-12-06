#include "../lib/temperature.hpp"

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

byte sensor1[8] = {0x10, 0xB4, 0xC9, 0x9A, 0x03, 0x08, 0x00, 0x99};
byte sensor2[8] = {0x10, 0x7C, 0x1C, 0x9A, 0x03, 0x08, 0x00, 0x2B};
byte sensor3[8] = {0x10, 0xBF, 0xD4, 0x9A, 0x03, 0x08, 0x00, 0xF1};

void temperatureSetup()
{
    // Set the power pin HIGH to power the DS18B20
    digitalWrite(POWER_PIN, HIGH);
    
    // Start up the library:
    sensors.begin();

    // Set the resolution for all devices to 9, 10, 11, or 12 bits:
    sensors.setResolution(12);
}

float getTemperature(DeviceAddress address)
{
    // Fetch the temperature in degrees Celsius for device address:
    return sensors.getTempC(address);
}

// Returns all temperatures in degrees Celsius
float *getTemperatures()
{
    // Call sensors.requestTemperatures() to issue a global temperature
    // request to all devices on the bus:
    sensors.requestTemperatures();

    // After we got the temperatures, we can print them here:
    float *temperatures = new float[3];
    temperatures[0] = getTemperature(sensor1);
    temperatures[1] = getTemperature(sensor2);
    temperatures[2] = getTemperature(sensor3);
    return temperatures;
}

void testTemperature()
{
    // Call sensors.requestTemperatures() to issue a global temperature
    // request to all devices on the bus:
    sensors.requestTemperatures();

    // After we got the temperatures, we can print them here:
    Serial.print("Temperature for the device 1 (index 0) is: ");
    Serial.println(getTemperature(sensor1));
    Serial.print("Temperature for the device 2 (index 1) is: ");
    Serial.println(getTemperature(sensor2));
    Serial.print("Temperature for the device 3 (index 2) is: ");
    Serial.println(getTemperature(sensor3));
}