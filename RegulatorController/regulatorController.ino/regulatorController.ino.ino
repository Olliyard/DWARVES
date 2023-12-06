// Includes
#include "OneWire.h"
#include "DallasTemperature.h"

// Declarations
#define PIN_C 7
#define PIN_B 5
#define PIN_A 6
#define PIN_INH 8
#define PIN_OUTPUT 9
#define ONE_WIRE_BUS A0
const byte numChars = 32;
const int numColonies = 3;
const int numChannels = 3;

char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// Create a new instance of the oneWire class to communicate with any OneWire device:
OneWire oneWire(ONE_WIRE_BUS);

// Pass the oneWire reference to DallasTemperature library:
DallasTemperature sensors(&oneWire);

// Variables
int dutyCycle[numColonies] = {0}; // 0 - red, 1 - blue, 2 - temp
int deviceCount = 0;
float tempC;
boolean newData = false;

struct colonies {
  int redBrightness = 0;
  int blueBrightness = 0;
  int setTemp = 0;
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PIN_C, OUTPUT);       // PIN-C
  pinMode(PIN_B, OUTPUT);       // PIN-B
  pinMode(PIN_A, OUTPUT);       // PIN-A
  pinMode(PIN_INH, OUTPUT);     // INH-PIN
  pinMode(PIN_OUTPUT, OUTPUT);  // IN

  // Initial state
  digitalWrite(PIN_A, LOW);
  digitalWrite(PIN_B, LOW);
  digitalWrite(PIN_C, LOW);
  digitalWrite(PIN_INH, HIGH);
  analogWrite(PIN_OUTPUT, dutyCycle);

  // Temperature reader setup
  sensors.begin();

  // Create colony struct array with maxColonies indexes. (colony1 = index 0 etc)
  struct Colony colonies[numColonies];
}


void loop() {
  int currColony = 0;                 // current colony handled
  recvData();                         // read the data
  if (newData == true){               // if newData flag has been set
    strcpy(tempChars, receivedChars); // make copy of original data
    currColony = parseData();         // parse the data and save the current colony
    setPWM(currColony, colonies[currColony].redBrightness, colonies[currColony].blueBrightness, colonies[currColony].setTemp);  // setPWM with the current colony struct settings.
    newData = false;                  // reset newData flag
  }
  delay(500); // Adjust the delay as needed
}


void setPWM(int colonyID, int red, int blue, int temp) {
  mapDutyCycle(red, blue, temp);
  digitalWrite(PIN_INH, LOW); // ON
  /* Would love to simplify lines 88 - 148 by using something similar to the below.
  for (colonyID=1; colonyID<=numColonies; colonyID++){
    digitalWrite(PIN_INH, LOW);

    for (int channel = 0; channel < numChannels; channel++) {
      digitalWrite(PIN_A, (channel & 0b001) ? HIGH : LOW);  // Set PIN_A based on the lowest bit of channel
      digitalWrite(PIN_B, (channel & 0b010) ? HIGH : LOW);  // Set PIN_B based on the second lowest bit of channel
      digitalWrite(PIN_C, (channel & 0b100) ? HIGH : LOW);  // Set PIN_C based on the third lowest bit of channel
      analogWrite(PIN_OUTPUT, dutyCycle[channel]);          // Set the duty cycle for the corresponding channel
      delay(100);
    }
    digitalWrite(PIN_INH, HIGH);
  }
  */

  // Set colony 1
  if (colonyID == 1) {
    // Set RED (channel 0)
    digitalWrite(PIN_INH, LOW); // ON
    digitalWrite(PIN_A, LOW);   // 0
    digitalWrite(PIN_B, LOW);   // 0
    digitalWrite(PIN_C, LOW);   // 0
    analogWrite(PIN_OUTPUT, dutyCycle[0]);

    // set BLUE (channel 1)
    digitalWrite(PIN_A, HIGH);  // 1
    digitalWrite(PIN_B, LOW);   // 0
    digitalWrite(PIN_C, LOW);   // 0
    analogWrite(PIN_OUTPUT, dutyCycle[1]);

    // Set TEMP (channel 2)
    digitalWrite(PIN_A, LOW);   // 0
    digitalWrite(PIN_B, HIGH);  // 1
    digitalWrite(PIN_C, LOW);   // 0
    analogWrite(PIN_OUTPUT, dutyCycle[2]);

    // Close MUX
    digitalWrite(PIN_INH, HIGH);
  }

  // Set colony 2
  else if (colonyID == 2) {
    // Set RED (channel 3)
    digitalWrite(PIN_INH, LOW);
    digitalWrite(PIN_A, HIGH);  // 1
    digitalWrite(PIN_B, HIGH);  // 1
    digitalWrite(PIN_C, LOW);   // 0
    analogWrite(PIN_OUTPUT, dutyCycle[0]);

    // Set BLUE (channel 4)
    digitalWrite(PIN_A, LOW);   // 0
    digitalWrite(PIN_B, LOW);   // 0
    digitalWrite(PIN_C, HIGH);  // 1
    analogWrite(PIN_OUTPUT, dutyCycle[1]);

    // Set TEMP (channel 5)
    digitalWrite(PIN_A, HIGH);  // 1
    digitalWrite(PIN_B, LOW);   // 0
    digitalWrite(PIN_C, HIGH);  // 1
    analogWrite(PIN_OUTPUT, dutyCycle[2]);
  }

  // Set colony 3
  else if (colonyID == 3) {
    // Set RED (channel 6)
    digitalWrite(PIN_INH, LOW);
    digitalWrite(PIN_A, LOW);   // 0
    digitalWrite(PIN_B, HIGH);  // 1
    digitalWrite(PIN_C, HIGH);  // 1
    analogWrite(PIN_OUTPUT, dutyCycle[0]);

    // Set BLUE (channel 7)
    digitalWrite(PIN_A, HIGH);  // 1
    digitalWrite(PIN_B, HIGH);  // 1
    digitalWrite(PIN_C, HIGH);  // 1
    analogWrite(PIN_OUTPUT, dutyCycle[1]);
  }
}

void mapDutyCycle(int red, int blue, int temp) {
  if (red > 0 || red < 100){
    dutyCycle[0] = map(red - '0', 0, 99, 0, 255);
  }
  if (blue > 0 || blue < 100){
    dutyCycle[1] = map(blue - '0', 0, 99, 0, 255);
  }
  if (temp > 0 || temp < 100){
    dutyCycle[2] = map(temp - '0', 0, 99, 0, 255);
  }
}

// Read data for given address
double tempRead(deviceAddr) {
  float temp = sensors.getTempC(deviceAddr);
}

// Receive data through serial connection
void recvData() {
    static boolean recvInProgress = false;  // Receive in progress
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

  while (Serial.available() > 0 && newData == false) {  // Read when serial available and not handling data
        rc = Serial.read();

        if (recvInProgress == true) { // if currently receiving data
            if (rc != endMarker) {    // if more data to receive read the received data into char array
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {  // else terminate string
                receivedChars[ndx] = '\0';
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) { // if start marker found in received data, start receiving process.
            recvInProgress = true;
        }
    }
}

// Parse received data and add to struct
int parseData() {
    char * strtokIndx;                                    // this is used by strtok() as an index
    int colonyID;
    strtokIndx = strtok(NULL, ",");                       // as int instead of string
    colonyID = atoi(strtokIndx-1);

    strtokIndx = strtok(NULL, ",");                       // this continues where the previous call left off
    colonies[colonyID].redBrightness = atoi(strtokIndx);  // convert and add to struct

    strtokIndx = strtok(NULL, ",");
    colonies[colonyID].blueBrigthness = atoi(strtokIndx); // convert and add to struct

    strtokIndx = strtok(NULL, ",");
    colonies[colonyID].setTemp = atoi(strtokIndx);        // convert and add to struct
    return colonyID
}