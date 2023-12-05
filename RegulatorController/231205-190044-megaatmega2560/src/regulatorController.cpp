// Includes
#include <Arduino.h>
// #include "../lib/temperature.hpp" // This is included in uart_handler.hpp
// #include "../lib/multiplexer.hpp" // This is included in uart_handler.hpp
#include "../lib/uart_handler.hpp"

void setup()
{
  // put your setup code here, to run once:
  setupUART();

  // Setup multiplexer
  multiplexerSetup();

  // Setup temperature sensor
  temperatureSetup();

  // testTemperature();
}

void loop()
{
  // put your main code here, to run repeatedly:
  handleUART();
  delay(3000);
}