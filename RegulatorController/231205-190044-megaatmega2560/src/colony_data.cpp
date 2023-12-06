#include "../lib/colony_data.hpp"

ColonyData colony1 = {100, 100, 100};
ColonyData colony2 = {0, 0, 0};
ColonyData colony3 = {0, 0, 0};

// Set values in structs
void setValues(int colonyID, int redBrightness, int blueBrightness, int setTemp)
{
    switch (colonyID)
    {
    case 1:
        colony1.redBrightness = redBrightness;
        colony1.blueBrightness = blueBrightness;
        colony1.heat = setTemp;
        break;
    case 2:
        colony2.redBrightness = redBrightness;
        colony2.blueBrightness = blueBrightness;
        colony2.heat = setTemp;
        break;
    case 3:
        colony3.redBrightness = redBrightness;
        colony3.blueBrightness = blueBrightness;
        colony3.heat = setTemp;
        break;
    }
}