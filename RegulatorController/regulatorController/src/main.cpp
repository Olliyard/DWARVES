#include "../lib/temperature.hpp"
#include "../lib/multiplexer.hpp"
#include "../lib/hx711.hpp"
#define COLONY_COUNT 4

// Global variables
HX711Wrapper hx711(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN, WEIGHT_THRESHOLD);
float temperature;
int weightStatus;

// CHARS TO RECEIVE
const byte numChars = 20;
char receivedChars[numChars];
char tempChars[numChars];     // temporary array for use when parsing
char command[numChars] = {0}; // Declare command globally
boolean newData = false;

struct Colony
{
  int redBrightness;
  int blueBrightness;
  float temperature;
  DeviceAddress temperatureAddress;
};

Colony colonies[COLONY_COUNT];
void recvData();
void parseData();

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  Serial.println("Initializing temperature sensor...");
  initTemperature();
  Serial.println("Temperature sensor initialized.");

  Serial.println("Setting up multiplexer...");
  multiplexerSetup();
  Serial.println("Multiplexer setup complete.");

  Serial.println("Initializing HX711...");
  hx711.initialize();
  Serial.println("HX711 initialized.");

  Serial.println("Getting addresses...");
  for (int i = 0; i < COLONY_COUNT; i++)
  {
    getAddress(i, colonies[i].temperatureAddress);
  }
  Serial.println("Addresses retrieved.");

  Serial.println("Ready");
}

void loop()
{
  recvData();
  if (newData == true)
  {
    strcpy(tempChars, receivedChars);
    parseData();
    newData = false;
  }
  // delay(500);
}

/* Receive data from Serial
Look for markers denoting start and end of message ('<' and '>') to ensure complete message is transfered
Check if start marker is present. If so, start receiving message until end marker is met. When met, terminate string.
*/
void recvData()
{
  static boolean recvInProgress = false; // False: not receiving, True: receiving
  static byte ndx = 0;                   // char indexer
  char startMarker = '<';                // custom start marker
  char endMarker = '>';                  // custom end marker
  char rc;                               // receive char

  while (Serial.available() > 0 && newData == false)
  {
    rc = Serial.read();

    if (recvInProgress == true)
    {
      if (rc != endMarker)
      { // No end marker met yet
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars)
        {
          ndx = numChars - 1;
        }
      }
      else
      { // Terminate string when end marker met
        receivedChars[ndx] = '\0';
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }
    else if (rc == startMarker)
    { // Only start receiving for start marker
      recvInProgress = true;
    }
  }
}

/* Parse data and look for commands/settings.
Accepted commands include:
<setl,colonyID,redLight,blueLight>  -- Sets the light for specified colony
<sett,colonyID,temp>                -- Sets the temperature for specified colony
<get,colonyID>                      -- Get colony values and obsTemp
Uses strtok (string token) to look through comma sepereated data. If command does not meet requirements, nothing happens.
Overflow protected.
*/
void parseData()
{
  char *strtokIndx;               // this is used by strtok() as an index
  uint8_t colonyID;
  strtokIndx = strtok(receivedChars, ",");
  strcpy(command, strtokIndx);    // copy it to command
  strtokIndx = strtok(NULL, ",");
  colonyID = atoi(strtokIndx);    // Extract colonyID from message
  Serial.println(command);        // Doesnt work without lol
  Serial.print("Value: ");        // same

  // SETT (set temp)
  if (strcmp(command, "sett") == 0)
  {
    // Only update the setTemp value
    strtokIndx = strtok(NULL, ",");
    colonies[colonyID].temperature = atoi(strtokIndx);
    Serial.print(colonies[colonyID].temperature);
    setTemperature(colonyID);
  }

  // SETL (set light)
  else if (strcmp(command, "setl") == 0)
  {
    // Update only redBrightness and blueBrightness values
    strtokIndx = strtok(NULL, ",");
    colonies[colonyID].redBrightness = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    colonies[colonyID].blueBrightness = atoi(strtokIndx);
    Serial.print("R");
    Serial.print(colonies[colonyID].redBrightness);
    Serial.print(" B");
    Serial.println(colonies[colonyID].blueBrightness);
    setBrightness(colonyID, colonies[colonyID].redBrightness, colonies[colonyID].blueBrightness);
  }

  // GET (get values)
  else if (strcmp(command, "get") == 0)
  {
    float temperature = getTemperature(colonies[colonyID].temperatureAddress);
    Serial.println(temperature);
    // Serial.println(colonies[colonyID].setTemp);  // Replace with get measured temperature method getTemperature(addr)
  }

  else if (strcmp(command, "lz") == 0)
  {
    Serial.println(hx711.getWeightStatus());
  }
}