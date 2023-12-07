#include "../lib/uart_handler.hpp"

void setupUART()
{
    Serial.begin(9600);
}

void handleUART()
{
    // Read the data
    String data = Serial.readStringUntil('\n');
    Serial.println(data);

    // Check for <setl,colonyID,red,blue>
    if (data.startsWith("<setl,"))
    {
        // Extract colonyID, red, blue. By dividing by comma
        data = data.substring(6); // Remove the "<setl," part
        int commaIndex1 = data.indexOf(',');
        int commaIndex2 = data.indexOf(',', commaIndex1 + 1);

        // Parse the data
        int colonyID = data.substring(0, commaIndex1).toInt();
        int red = data.substring(commaIndex1 + 1, commaIndex2).toInt();
        int blue = data.substring(commaIndex2 + 1, data.length() - 1).toInt(); // Subtract 1 to remove the closing '>'

        /*         Serial.print("Colony ID: ");
                Serial.println(colonyID);
                Serial.print("Red brightness: ");
                Serial.println(red);
                Serial.print("Blue brightness: ");
                Serial.println(blue); */

        // Set the values
        setValuesBrightness(colonyID, red, blue);
    }
    // Check for <sett,colonyID,temp>
    else if (data.startsWith("<sett"))
    {
        // Extract colonyID, temp. By dividing by comma
        data = data.substring(6); // Remove the "<sett," part
        int commaIndex = data.indexOf(',');
        int colonyID = data.substring(0, commaIndex).toInt();
        int temp = data.substring(commaIndex + 1, data.length() - 1).toInt(); // Subtract 1 to remove the closing '>'

        /*         Serial.print("Colony ID: ");
                Serial.println(colonyID);
                Serial.print("Set temperature: ");
                Serial.println(temp); */

        // Set the values
        setValuesTemp(colonyID, temp);
    }

    // Check for <get,colonyID>
    else if (data.startsWith("<get,"))
    {
        // Extract colonyID. By dividing by comma
        data = data.substring(5);                                    // Remove the "<get," part
        int colonyID = data.substring(0, data.length() - 1).toInt(); // Subtract 1 to remove the closing '>'
        Serial.print("Colony ID hereere: ");
        Serial.println(colonyID);

        // Send the temperatures
        float temperature = getTemperature(colonyID);
        Serial.print(temperature);
    }

    else
    {
        Serial.println("ERROR: Invalid protocol");
    }
}

void serialEvent()
{
    while (Serial.available())
    {
        // Call handleUART() when data is available
        handleUART();
    }
}

// React to the data
void react()
{
    // Set the brightness for all the colonies
    setBrightness(1, colony1.redBrightness, colony1.blueBrightness);
    setBrightness(2, colony2.redBrightness, colony2.blueBrightness);
    setBrightness(3, colony3.redBrightness, colony3.blueBrightness);

    // Check the temperatures, if they are less than the set temperature, turn heat onto max:
    float *temperatures = getTemperatures();
    if (temperatures[0] < colony1.heat)
    {
        setTemperature(1);
    }
    else if (temperatures[1] < colony2.heat)
    {
        setTemperature(2);
    }
    else if (temperatures[2] < colony3.heat)
    {
        setTemperature(3);
    }
}

void sendTemperatures()
{
    // Get the temperatures
    float *temperatures = getTemperatures();

    // Send the temperatures
    Serial.print(temperatures[0]);
    Serial.print(",");
    Serial.print(temperatures[1]);
    Serial.print(",");
    Serial.println(temperatures[2]);
}

void printSettings(int colonyID, int redBrightness, int blueBrightness, int setTemp)
{
    Serial.print("Colony ID: ");
    Serial.println(colonyID);
    Serial.print("Red brightness: ");
    Serial.println(redBrightness);
    Serial.print("Blue brightness: ");
    Serial.println(blueBrightness);
    Serial.print("Set temperature: ");
    Serial.println(setTemp);
    Serial.println("\n");
}
