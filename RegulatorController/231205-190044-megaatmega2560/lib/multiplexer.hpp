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

void mapValue(uint8_t value); // Map a value to graph for transistor turn on

void setBrightness(uint8_t colonyID, uint8_t brightnessRed, uint8_t brightnessBlue); // Set the light for a colony
void setTemperature(uint8_t colonyID, uint8_t heat); // Set the temperature for a colony
void testsetTemperature(uint8_t colonyID, uint8_t heat); // Test function for setting temperature

void test_stepwise_increment_colony1_red(); // Test function for stepwise incrementing colony 1
void test_stepwise_increment_colony1_blue();
void test_stepwise_increment_colony1_temp();