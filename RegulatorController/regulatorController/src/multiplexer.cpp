#include "../lib/multiplexer.hpp"

void multiplexerSetup()
{
    Serial.println("Initializing multiplexer");
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
    // Serial.println("Resetting multiplexer...");
    delay(switchDelay);
    analogWrite(PIN_OUTPUT, 0);
    digitalWrite(PIN_INH, HIGH);
    delay(switchDelay);
}

void setBrightness(uint8_t colonyID, uint8_t brightnessRed, uint8_t brightnessBlue)
{
    // Map the brightness values from 0-100 to 0-255
    brightnessRed = fluxToAnalogValue(brightnessRed);
    brightnessBlue = fluxToAnalogValue(brightnessBlue);

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

    Serial.print("Setting brightness for colony ");
    Serial.println(colonyID);
}

void setTemperature(uint8_t colonyID)
{
    switch (colonyID)
    {
    case 1:
        // Set TEMP (channel 6)
        digitalWrite(PIN_A, LOW);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, 255); // 100% duty cycle
        resetMultiplexer();
        break;

    case 2:
        // Set TEMP (channel 7)
        digitalWrite(PIN_A, HIGH);
        digitalWrite(PIN_B, HIGH);
        digitalWrite(PIN_C, HIGH);
        digitalWrite(PIN_INH, LOW);
        analogWrite(PIN_OUTPUT, 255); // 100% duty cycle
        resetMultiplexer(); 
        break;

    case 3:
        // Set TEMP (pin_temp_3)
        analogWrite(pin_temp_3, 255);
        resetMultiplexer();
    }

    Serial.print("Setting temperature for colony ");
    Serial.println(colonyID);
}

float fluxToAnalogValue(float flux)
{
    Serial.println("Converting flux to analog value...");
    if (flux == 0) // To make sure that voltage is zero when flux is zero
    {
        return 0;
    }
    // Coefficients obtained from linear regression
    // duty_cycle = 0.36 * flux + 50.0
    float a = 0.36;
    float b = 50.0;

    // Map the flux values from 0-100 to 0-255
    uint8_t dutyCycle = a * flux + b;
    // Serial.print("Duty cycle: ");
    // Serial.println(dutyCycle);
    uint8_t analogValue = map(dutyCycle, 0, 100, 0, 255);
    // Serial.print("Analog value: ");
    // Serial.println(analogValue);
    return analogValue;
}

void test_stepwise_increment_colony1_red()
{
    Serial.println("Testing stepwise increment of colony 1 red");

    // Set brightness
    digitalWrite(PIN_A, LOW);
    digitalWrite(PIN_B, LOW);
    digitalWrite(PIN_C, LOW);
    digitalWrite(PIN_INH, LOW);
    int analogValue = 0;
    // For loop to increment red brightness
    for (int i = 0; i <= 100; i++)
    {
        analogValue = map(i, 0, 100, 0, 255);
        analogWrite(PIN_OUTPUT, analogValue);
        // Print Current values
        Serial.print("Current red brightness: ");
        Serial.println(i);

        // Press enter to continue
        while (!Serial.available())
        {
            delay(1000);
        }
        Serial.read();
    }
}

void test_stepwise_increment_colony1_blue()
{
    Serial.println("Testing stepwise increment of colony 1 blue");

    // Set brightness
    digitalWrite(PIN_A, HIGH);
    digitalWrite(PIN_B, LOW);
    digitalWrite(PIN_C, LOW);
    digitalWrite(PIN_INH, LOW);
    int analogValue = 0;
    // For loop to increment red brightness
    for (int i = 0; i <= 100; i++)
    {
        analogValue = map(i, 0, 100, 0, 255);
        analogWrite(PIN_OUTPUT, analogValue);
        // Print Current values
        Serial.print("Current blue brightness: ");
        Serial.println(i);

        // Press enter to continue
        while (!Serial.available())
        {
            delay(1000);
        }
        Serial.read();
    }
}

void test_stepwise_increment_colony1_temp()
{
    Serial.println("Testing stepwise increment of colony 1 temp");

    // Set temperature
    digitalWrite(PIN_A, LOW);
    digitalWrite(PIN_B, HIGH);
    digitalWrite(PIN_C, HIGH);
    digitalWrite(PIN_INH, LOW);
    int analogValue = 0;
    // For loop to increment red brightness
    for (int i = 0; i <= 100; i++)
    {
        analogValue = map(i, 0, 100, 0, 255);
        analogWrite(PIN_OUTPUT, analogValue);
        // Print Current values
        Serial.print("Current temp: ");
        Serial.println(i);

        // Press enter to continue
        while (!Serial.available())
        {
            delay(1000);
        }
        Serial.read();
    }
}