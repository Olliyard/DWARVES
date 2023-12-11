#include "../lib/temperature.hpp"

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void initTemperature()
{
    // Set pins
    pinMode(POWER_PIN, OUTPUT);
    digitalWrite(POWER_PIN, HIGH);

    // Start up the library
    sensors.begin();
    sensors.setResolution(12);
}

float getTemperature(DeviceAddress deviceAddress)
{
    // Start up the library
    sensors.requestTemperatures();
    return sensors.getTempC(deviceAddress);
}

// Return address for a given colony. Use the getAddress function from DallasTemperature library
void getAddress(int colonyID, DeviceAddress& deviceAddress)
{
    sensors.getAddress(deviceAddress, colonyID);
}
