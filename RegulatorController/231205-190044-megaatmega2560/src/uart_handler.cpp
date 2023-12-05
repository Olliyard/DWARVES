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

            // React to the data
            react(colonyID, redBrightness, blueBrightness, setTemp);
        }

        else
        {
            Serial.println("ERROR: Invalid protocol");
        }
    }
}

void react(int colonyID, int redBrightness, int blueBrightness, int setTemp)
{
    // Set the brightness
    setBrightness(colonyID, redBrightness, blueBrightness);

    // Set the temperature
    setTemperature(colonyID, setTemp);

    // Print "OK"
    Serial.println("OK"); // Host knows that the settings were applied
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
