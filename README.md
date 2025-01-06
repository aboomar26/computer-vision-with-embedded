# Arduino LED Control and LCD Display Project

## Project Overview
This project is a multi-functional Arduino-based system that:
1. Controls LEDs to represent the states of fingers on both hands.
2. Uses an I2C-enabled LCD display to show the number of active fingers for the right hand, left hand, and the total count.
3. Communicates with a computer through Serial communication to receive and process hand states.

The system uses an Arduino Uno, an I2C LCD module, and 10 LEDs. Data is transmitted via Serial in the form of a custom string format, and the system processes the data to control the LEDs and update the LCD.

## Features
- **LED Indicators:** Visualize the states of individual fingers on both hands.
- **LCD Display:** Displays counts of active fingers and their sum.
- **Serial Communication:** Receives data about finger states from an external source.

## Components Used
### Hardware
- Arduino Uno
- I2C-enabled 16x2 LCD module
- 10 LEDs (5 for each hand)
- Resistors (appropriate values for LEDs)
- Breadboards
- Jumper wires

### Software
- Arduino IDE
- Python GUI application for interaction (Tkinter-based with PyTorch for food detection as an additional feature)

---

## Wiring Connections
### LED Connections
- **Right-hand LEDs:** Connected to digital pins 2, 3, 4, 5, 6
- **Left-hand LEDs:** Connected to digital pins 7, 8, 9, 10, 11

### LCD Connections
- LCD SDA -> Arduino A4
- LCD SCL -> Arduino A5
- LCD VCC -> Arduino 5V
- LCD GND -> Arduino GND

Refer to the provided schematic image `connections.jpg` for detailed wiring.

---

## Arduino Code
The Arduino code handles:
1. Receiving serialized data through the Serial port.
2. Controlling LEDs based on the received data.
3. Updating the LCD display with the count of active fingers.

### Code Highlights
- `LiquidCrystal_I2C` library is used for LCD control.
- Data is received in the format `$0000000000`, where each digit represents the state of a finger (1 for active, 0 for inactive).
- LEDs are controlled using `digitalWrite` based on the processed data.

#### Embedded Code
```cpp
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

LiquidCrystal_I2C lcd(0x27, 16, 2);

int lastRightCount = -1;
int lastLeftCount = -1;
int lastSum = -1;

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Welcome");
  delay(2000);
  lcd.clear();

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
      receivedString = "";
      counter = 0;
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

  for (int i = 0; i < 5; i++) {
    if (valsRec[i] == 1) rightCount++;
    if (valsRec[i + 5] == 1) leftCount++;
  }

  int total = rightCount + leftCount;

  if (rightCount != lastRightCount || leftCount != lastLeftCount || total != lastSum) {
    lcd.setCursor(0, 0);
    lcd.print("R: ");
    lcd.print(rightCount);
    lcd.print(" L: ");
    lcd.print(leftCount);
    lcd.setCursor(0, 1);
    lcd.print("Sum: ");
    lcd.print(total);
    lcd.print("    ");

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
```

---

## Python GUI Application
An additional Python application allows you to interact with the Arduino project. It features:
- Tkinter-based GUI
- Upload image functionality with pre-trained ResNet food detection
- Display of predictions with confidence levels

### Python Code
Refer to the provided Python script for details.

---

## How to Use
1. Assemble the circuit as per the schematic.
2. Upload the Arduino sketch using Arduino IDE.
3. Run the Python application to visualize and interact with the system.

## Future Enhancements
- Add gesture recognition through advanced input devices.
- Improve data visualization on the LCD with scrolling text.

---

## Author
**Abdallah Abouomar**

If you have any questions or improvements, feel free to raise an issue or submit a pull request on this repository!
