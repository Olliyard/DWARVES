// declearations
#define PIN_C 7
#define PIN_B 5
#define PIN_A 6
#define PIN_INH 8
#define PIN_OUTPUT 9

char input;

int dutyCycle = 0;

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
  digitalWrite(PIN_B, HIGH);
  digitalWrite(PIN_C, LOW);
  digitalWrite(PIN_INH, HIGH);
  analogWrite(PIN_OUTPUT, dutyCycle);

  // Initial print
  printValues();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    input = Serial.read();
    
    // Toggle channels on A, B, C, and INH
    if (input == 'A' || input == 'a') {
      digitalWrite(PIN_A, !digitalRead(PIN_A));
    } else if (input == 'B' || input == 'b') {
      digitalWrite(PIN_B, !digitalRead(PIN_B));
    } else if (input == 'C' || input == 'c') {
      digitalWrite(PIN_C, !digitalRead(PIN_C));
    } else if (input == 'I' || input == 'i') {
      digitalWrite(PIN_INH, !digitalRead(PIN_INH));
    }
    
    // Set duty cycle for analogWrite
    if (input >= '0' && input <= '9') {
      dutyCycle = map(input - '0', 0, 9, 0, 255);
      analogWrite(PIN_OUTPUT, dutyCycle);
    }

    // Print new values
    printValues();
  }

  delay(500); // Adjust the delay as needed
}

void printValues() {
  Serial.print("A: ");
  Serial.print(digitalRead(PIN_A));
  Serial.print(", B: ");
  Serial.print(digitalRead(PIN_B));
  Serial.print(", C: ");
  Serial.print(digitalRead(PIN_C));
  Serial.print(", INH: ");
  Serial.print(digitalRead(PIN_INH));
  Serial.print(", Duty Cycle: ");
  Serial.print(map(dutyCycle, 0, 255, 0, 100)); // Map duty cycle back to percentage
  Serial.println("%");
}
