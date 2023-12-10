#pragma once
#include <Arduino.h>

// Declarations
#define switchDelay 100 // Delay between switching channels
#define PIN_C 7 // Most significant bit
#define PIN_B 5 // Middle bit
#define PIN_A 6 // Least significant bit
#define PIN_INH 8 // Inhibit, active low
#define PIN_OUTPUT 9 // PWM Output pin
#define pin_temp_3 10 // Temperature set pin for colony 3

// Functions
void multiplexerSetup(); // Setup function for multiplexer
void resetMultiplexer(); // Reset multiplexer

float fluxToAnalogValue(float flux); // Convert flux to analog value

void setBrightness(uint8_t colonyID, uint8_t brightnessRed, uint8_t brightnessBlue); // Set the light for a colony
void setTemperature(uint8_t colonyID); // Turn on the heating element for a colony

// Test functions
void test_stepwise_increment_colony1_red(); // Test function for stepwise incrementing colony 1
void test_stepwise_increment_colony1_blue();
void test_stepwise_increment_colony1_temp();