#pragma once

void setValues(int colonyID, int redBrightness, int blueBrightness, int setTemp);

struct ColonyData
{
    int redBrightness;
    int blueBrightness;
    int heat;
};

extern ColonyData colony1;
extern ColonyData colony2;
extern ColonyData colony3;