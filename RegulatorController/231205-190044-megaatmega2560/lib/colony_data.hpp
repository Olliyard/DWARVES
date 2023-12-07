#pragma once


void setValuesBrightness(int colonyID, int redBrightness, int blueBrightness);
void setValuesTemp(int colonyID, int temp);


struct ColonyData
{
    int redBrightness; // relative flux 0-100%
    int blueBrightness; // relative flux 0-100%
    int heat; // wanted heat in degrees C
};

extern ColonyData colony1;
extern ColonyData colony2;
extern ColonyData colony3;