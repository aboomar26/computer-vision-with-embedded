#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define numOfValsRec 10
#define digitsPerValRec 1

const int ledRightHand[5] = {2, 3, 4, 5, 6};  // LEDs for right-hand fingers
const int ledLeftHand[5] = {7, 8, 9, 10, 11}; // LEDs for left-hand fingers

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1;  // Format: $0000000000
int counter = 0;
bool counterStart = false;
String receivedString;

// Initialize the LCD (adjust the address to your LCD, e.g., 0x27 or 0x3F)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Variables to track LCD updates
int lastRightCount = -1;
int lastLeftCount = -1;
int lastSum = -1;

void setup() {
  Serial.begin(9600);

  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Welcome");
  delay(2000);  // Display welcome message for 2 seconds
  lcd.clear();

  // Initialize LED pins
  for (int i = 0; i < 5; i++) {
    pinMode(ledRightHand[i], OUTPUT);
    pinMode(ledLeftHand[i], OUTPUT);
  }
}

void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '$') {
      counterStart = true;
      receivedString = ""; // Reset string to prevent stale data
      counter = 0; // Reset counter
    }
    if (counterStart) {
      receivedString += c;
      counter++;
      if (counter >= stringLength) {
        for (int i = 0; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
        }
        counterStart = false;
      }
    }
  }
}

void controlLEDs() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(ledRightHand[i], valsRec[i] == 1 ? HIGH : LOW);
    digitalWrite(ledLeftHand[i], valsRec[i + 5] == 1 ? HIGH : LOW);
  }
}

void updateLCD() {
  int rightCount = 0;
  int leftCount = 0;

  // Count fingers for each hand
  for (int i = 0; i < 5; i++) {
    if (valsRec[i] == 1) rightCount++;       // Right hand
    if (valsRec[i + 5] == 1) leftCount++;   // Left hand
  }

  int total = rightCount + leftCount;

  // Update LCD only if there is a change
  if (rightCount != lastRightCount || leftCount != lastLeftCount || total != lastSum) {
    lcd.setCursor(0, 0);
    lcd.print("R: ");
    lcd.print(rightCount);
    lcd.print(" L: ");
    lcd.print(leftCount);
    lcd.setCursor(0, 1);
    lcd.print("Sum: ");
    lcd.print(total);
    lcd.print("    "); // Clear extra characters from previous display

    // Update tracking variables
    lastRightCount = rightCount;
    lastLeftCount = leftCount;
    lastSum = total;
  }
}

void loop() {
  receiveData();
  controlLEDs();
  updateLCD();
}

