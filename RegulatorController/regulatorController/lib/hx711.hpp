#pragma once

#include <HX711.h>

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
const float WEIGHT_THRESHOLD = 10.0; // Set your desired threshold

class HX711Wrapper
{
public:
    HX711Wrapper(int doutPin, int sckPin, float threshold);

    void initialize();
    int getWeightStatus();

private:
    HX711 scale;
    float weightThreshold;
};
