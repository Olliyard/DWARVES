#pragma once
#include <Arduino.h>
#include "../lib/multiplexer.hpp"
#include "../lib/temperature.hpp"
#include "../lib/colony_data.hpp"
#include "../lib/loadingsensor.hpp"


// Protocol;
/* set:
<setl,colonyID,red,blue>
<sett,colonyID,temp>

get:
<get,colonyID> */

void setupUART();
void handleUART();
void react();
void sendTemperatures();
void printSettings(int colonyID, int redBrightness, int blueBrightness, int setTemp);
void sendLoadingZoneStatus();
