#include "../lib/loadingsensor.hpp"

HX711Wrapper::HX711Wrapper(int doutPin, int sckPin, float threshold)
{
	scale.begin(doutPin, sckPin);
	weightThreshold = threshold;
}

void HX711Wrapper::initialize()
{
	scale.set_scale(2280.f);
	scale.tare();
}

int HX711Wrapper::getWeightStatus()
{
	float weight = scale.get_units(5);
	Serial.println(weight);
	return (weight > weightThreshold ? 1 : 0);
}
