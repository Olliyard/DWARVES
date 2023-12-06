#include "../lib/multiplexer.hpp"

void multiplexerSetup()
{
    // put your setup code here, to run once:
    pinMode(PIN_C, OUTPUT);      // PIN-C
    pinMode(PIN_B, OUTPUT);      // PIN-B
    pinMode(PIN_A, OUTPUT);      // PIN-A
    pinMode(PIN_INH, OUTPUT);    // INH-PIN
    pinMode(PIN_OUTPUT, OUTPUT); // IN

    // Initial state
    resetMultiplexer();
}

void resetMultiplexer()
{
    delay(switchDelay);
    analogWrite(PIN_OUTPUT, 0);
    digitalWrite(PIN_INH, HIGH);
    delay(switchDelay);
}

void setBrightness(uint8_t colonyID, uint8_t brightnessRed, uint8_t brightnessBlue)
{
    // Map the brightness values from 0-100 to 0-255
    brightnessRed = map(brightnessRed, 0, 100, 0, 255);
    brightnessBlue = map(brightnessBlue, 0, 100, 0, 255);

    // Print the values
    /*
    Serial.print("Red brightness: ");
    Serial.println(brightnessRed);
    Serial.print("Blue brightness: ");
    Serial.println(brightnessBlue);
    */

    switch (colonyID)
    {
    case 1:
        // Set RED (channel 0)
        digitalWrite(PIN_A, LOW);
        digitalWrite(PIN_B, LOW);
        digitalWrite(PIN_C, LOW);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, brightnessRed);
        resetMultiplexer();

        // set BLUE (channel 1)
        digitalWrite(PIN_A, HIGH);
        digitalWrite(PIN_B, LOW);
        digitalWrite(PIN_C, LOW);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, brightnessBlue);
        resetMultiplexer();
        break;

    case 2:
        // Set RED (channel 2)
        digitalWrite(PIN_A, LOW);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, LOW);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, brightnessRed);

        resetMultiplexer();

        // set BLUE (channel 3)
        digitalWrite(PIN_A, HIGH);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, LOW);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, brightnessBlue);

        resetMultiplexer();
        break;

    case 3:
        // Set RED (channel 4)
        digitalWrite(PIN_A, LOW);
        digitalWrite(PIN_B, LOW);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, brightnessRed);

        resetMultiplexer();

        // set BLUE (channel 5)
        digitalWrite(PIN_A, HIGH);
        digitalWrite(PIN_B, LOW);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, brightnessBlue);

        resetMultiplexer();
    }
}

void setTemperature(uint8_t colonyID, uint8_t heat)
{
    // Map the heat values from 0-100 to 0-255
    heat = map(heat, 0, 100, 0, 255);

    switch (colonyID)
    {
    case 1:
        // Set TEMP (channel 6)
        digitalWrite(PIN_A, LOW);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, heat);
        resetMultiplexer();
        break;

    case 2:
        // Set TEMP (channel 7)
        digitalWrite(PIN_A, HIGH);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, heat);
        resetMultiplexer();
        break;

    case 3:
        // Set TEMP (pin_temp_3)
        analogWrite(pin_temp_3, heat);
        resetMultiplexer();
    }
}

// to be tested. Replace with actual values from tests.
void testsetTemperature(uint8_t colonyID, uint8_t heat)
{
    // Coefficients obtained from linear regression
    float m = 0.021; // Replace with your actual value
    float b = 1.7;   // Replace with your actual value

    // Map the heat values from 0-100 to 0-255
    heat = m * heat + b;
    heat = map(heat, 1.7, 5, 0, 255);

    switch (colonyID)
    {
    case 1:
        // Set TEMP (channel 6)
        digitalWrite(PIN_A, LOW);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, heat);
        delay(switchDelay);
        resetMultiplexer();
        break;

    case 2:
        // Set TEMP (channel 7)
        digitalWrite(PIN_A, HIGH);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, HIGH);
        // ... rest of your code
    }
}