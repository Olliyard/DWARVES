#include "../lib/uart_handler.hpp"

void setupUART()
{
    Serial.begin(9600);
}

void handleUART()
{
    if (Serial.available())
    {                                               // If data is available to read
        String data = Serial.readStringUntil('\n'); // Read the data until a newline character
        Serial.println(data);

        // Protocol: "t" means get temperatures, data[0] = s means set settings
        if (data[0] == 't')
        {
            sendTemperatures();
            return;
        }

        else if (data[0] == 's')
        {
            // Find the indices of the commas
            int commaIndex0 = data.indexOf(',');
            int commaIndex1 = data.indexOf(',', commaIndex0 + 1);
            int commaIndex2 = data.indexOf(',', commaIndex1 + 1);
            int commaIndex3 = data.indexOf(',', commaIndex2 + 1);

            // Parse the data
            int colonyID = data.substring(commaIndex0 + 1, commaIndex1).toInt();
            int redBrightness = data.substring(commaIndex1 + 1, commaIndex2).toInt();
            int blueBrightness = data.substring(commaIndex2 + 1, commaIndex3).toInt();
            int setTemp = data.substring(commaIndex3 + 1).toInt();

            // For debug: Call a function to print based on these values
            printSettings(colonyID, redBrightness, blueBrightness, setTemp);

            // Set the values in the struct
            setValues(colonyID, redBrightness, blueBrightness, setTemp);

            // Print "OK"
            Serial.println("OK"); // Host knows that the settings were applied
        }

        else
        {
            Serial.println("ERROR: Invalid protocol");
        }
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

    // Set the temperature for all the colonies
    setTemperature(1, colony1.heat);
    setTemperature(2, colony2.heat);
    setTemperature(3, colony3.heat);
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
