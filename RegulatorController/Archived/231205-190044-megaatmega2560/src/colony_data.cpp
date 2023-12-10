#include "../lib/colony_data.hpp"

ColonyData colony1 = {100, 0, 0};
ColonyData colony2 = {0, 0, 0};
ColonyData colony3 = {0, 0, 0};

void setValuesBrightness(int colonyID, int redBrightness, int blueBrightness)
{
    switch (colonyID)
    {
    case 1:
        colony1.redBrightness = redBrightness;
        colony1.blueBrightness = blueBrightness;
        break;
    case 2:
        colony2.redBrightness = redBrightness;
        colony2.blueBrightness = blueBrightness;
        break;
    case 3:
        colony3.redBrightness = redBrightness;
        colony3.blueBrightness = blueBrightness;
        break;
    }
}

void setValuesTemp(int colonyID, int temp)
{
    switch (colonyID)
    {
    case 1:
        colony1.heat = temp;
        break;
    case 2:
        colony2.heat = temp;
        break;
    case 3:
        colony3.heat = temp;
        break;
    }
}


