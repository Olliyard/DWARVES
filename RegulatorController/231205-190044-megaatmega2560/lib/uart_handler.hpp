#pragma once
#include <Arduino.h>
#include "../lib/multiplexer.hpp"
#include "../lib/temperature.hpp"
#include "../lib/colony_data.hpp"


// Protocol;
// <t> -> get temperatures
// example: t
// <s> -> set settings: <command>, <colonyID (1 to 3), redBrightness (percentage), blueBrightness (percentage), setTemp (percentage)>
// example: s,1,100,100,100

void setupUART();
void handleUART();
void react();
void sendTemperatures();
void printSettings(int colonyID, int redBrightness, int blueBrightness, int setTemp);